# -*- coding: utf-8 -*-

"""
Findref data models.

Version: 0.2.1
"""

import typing as T
import enum
import json
import dataclasses
from pathlib import Path
from urllib import request

import sayt.api as sayt


T_DATA = T.Dict[str, T.Any]


class DataSetEnum(str, enum.Enum):
    airflow = "airflow"  # Airflow
    aws_cloudformation = "aws_cloudformation"  # AWS CloudFormation
    boto3 = "boto3"  # AWS Python SDK - boto3
    cdk_python = "cdk_python"  # AWS CDK Python
    cdk_ts = "cdk_ts"  # AWS CDK TypeScript
    pyspark = "pyspark"  # PySpark
    pandas = "pandas"  # Pandas
    tf = "tf"  # Terraform


@dataclasses.dataclass
class BaseModel:
    def to_dict(self) -> T.Dict[str, T.Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, dct: T.Dict[str, T.Any]):
        return cls(**dct)


@dataclasses.dataclass
class Metadata(BaseModel):
    dataset_name: str = dataclasses.field()


@dataclasses.dataclass
class Release(BaseModel):
    """
    :param metadata: metadata object.
    :param docs: list of documents, each document is a Python dict.
    """

    metadata: Metadata
    docs: T.List[T.Dict[str, T.Any]]

    def to_binary(self) -> bytes:
        dct = {
            "metadata": self.metadata.to_dict(),
            "docs": self.docs,
        }
        return json.dumps(dct, sort_keys=True, ensure_ascii=False).encode("utf-8")

    @classmethod
    def from_binary(cls, binary: bytes):
        data = json.loads(binary.decode("utf-8"))
        data["metadata"] = Metadata.from_dict(data["metadata"])
        return cls(**data)


# ------------------------------------------------------------------------------
# List of dataset models
#
# For each dataset, it has to have the following variables:
# 1. ``class ${DataSetName}Record``
# 2. ``class ${DataSetName}Document``
# 3. ``${DataSetName}_fields``
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class BaseRecord(BaseModel):
    @property
    def sort_key(self) -> str:
        raise NotImplementedError

    @classmethod
    def sort_by_sort_keys(cls, records) -> T.Iterable:
        return sorted(
            records,
            key=lambda record: record.sort_key,
        )


@dataclasses.dataclass
class BaseDocument(BaseModel):
    @property
    def uid(self) -> str:
        raise NotImplementedError

    @property
    def title(self) -> str:
        raise NotImplementedError

    @property
    def subtitle(self) -> str:
        raise NotImplementedError

    @property
    def arg(self) -> str:
        raise NotImplementedError

    @property
    def autocomplete(self) -> str:
        raise NotImplementedError


_title_to_autocomplete_delimiters = "_-.|@+"


@dataclasses.dataclass
class CommonDocument(BaseDocument):
    @property
    def uid(self) -> str:
        return self.url

    @property
    def subtitle(self) -> str:
        return f"Tap 'Enter' to open: 🌐 {self.url}"

    @property
    def arg(self) -> str:
        return self.url

    @property
    def autocomplete(self) -> str:
        """
        Characters like "_-.|@+" in the default whoosh query language has
        special meaning, the query text should only use space as delimiter.
        """
        s = self.title
        for char in _title_to_autocomplete_delimiters:
            s = s.replace(char, " ")
        return " ".join([word.strip() for word in s.split() if word.strip()])


def tokenify(s: str) -> str:
    """
    Sometimes the default tokenizer analyzer is not good enough, we need to
    preprocess the TextField before indexing it.
    """
    for char in "._-":
        s = s.replace(char, " ")
    return s


# ------------------------------------------------------------------------------
# Airflow
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class AirflowRecord(BaseRecord):
    """
    Example:

    - doc url: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/s3/index.html
    - doc source: https://github.com/apache/airflow/blob/main/docs/apache-airflow-providers-amazon/operators/s3/index.rst

    :param url: see above
    :param sub_doc: the name of the sub documentation site, in this example, it is ``"providers-amazon"``.
        with ``"apache-airflow-"`` stripped.
    :param title: the header title in the *.rst file, in this example, it is ``"Amazon S3 Operators"``.
    """

    url: str
    sub_doc: str
    title: str

    @property
    def sort_key(self) -> str:
        return self.url

    def to_doc(self) -> "AirflowDocument":
        return AirflowDocument(
            url=self.url,
            sub_doc=tokenify(self.sub_doc),
            sub_doc_ng=self.sub_doc,
            header=tokenify(self.title),
            header_ng=self.title,
        )


@dataclasses.dataclass
class AirflowDocument(CommonDocument):
    """
    Example:

    - doc url: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/s3/index.html
    - doc source: https://github.com/apache/airflow/blob/main/docs/apache-airflow-providers-amazon/operators/s3/index.rst

    :param url: same as :attr:`AirflowRecord.url`
    :param sub_doc: same as :attr:`AirflowRecord.sub_doc`
    :param sub_doc_ng: same as :attr:`AirflowRecord.sub_doc`
    :param header: same as :attr:`AirflowRecord.title`
    :param header_ng: same as :attr:`AirflowRecord.title`
    """

    url: str
    sub_doc: str
    sub_doc_ng: str
    header: str
    header_ng: str

    @property
    def title(self) -> str:
        return f"{self.sub_doc_ng} | {self.header_ng}"


airflow_fields = [
    sayt.StoredField(
        name="url",
    ),
    sayt.TextField(
        name="sub_doc",
        stored=True,
        field_boost=5.0,
    ),
    sayt.NgramWordsField(
        name="sub_doc_ng",
        stored=True,
        field_boost=5.0,
        minsize=2,
        maxsize=6,
    ),
    sayt.TextField(
        name="header",
        stored=True,
    ),
    sayt.NgramWordsField(
        name="header_ng",
        stored=True,
        minsize=2,
        maxsize=6,
    ),
]


# ------------------------------------------------------------------------------
# AWS CloudFormation
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class AwsCloudFormationRecord(BaseRecord):
    """
    Example: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html

    :param url: the url of the AWS resource CloudFormation document
        In this example, it is https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html
    :param type: property or resource.
    :param service: the service name in the ``AWS::${Service}::${Resource}``
        In this example, it is ``"S3"``
    :param resource: the resource name in the ``AWS::${Service}::${Resource}``
        In this example, it is ``"Bucket"``
    :param property: the resource name in the ``AWS::${Service}::${Resource}.${Property}``
        In this example, it is ``"BucketEncryption"``
    """

    url: str
    type: str
    service: str
    resource: str
    prop: T.Optional[str] = dataclasses.field(default=None)

    @property
    def sort_key(self) -> str:
        return " ".join([self.type, self.service, self.resource, str(self.prop)])

    def to_doc(self) -> "AwsCloudFormationDocument":
        return AwsCloudFormationDocument(
            url=self.url,
            type=self.type,
            type_ng=self.type,
            srv=self.service,
            srv_ng=self.service,
            res=self.resource,
            res_ng=self.resource,
            prop=self.prop,
            prop_ng=self.prop,
        )


@dataclasses.dataclass
class AwsCloudFormationDocument(CommonDocument):
    """
    Example: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html

    :param url: same as :attr:`AwsCloudFormationRecord.url``
    :param type: same as :attr:`AwsCloudFormationRecord.type``
    :param type_ng: same as :attr:`AwsCloudFormationRecord.type``
    :param srv: same as :attr:`AwsCloudFormationRecord.service``
    :param srv_ng: same as :attr:`AwsCloudFormationRecord.service``
    :param res: same as :attr:`AwsCloudFormationRecord.resource``
    :param res_ng: same as :attr:`AwsCloudFormationRecord.resource``
    :param prop: same as :attr:`AwsCloudFormationRecord.prop``
    :param prop_ng: same as :attr:`AwsCloudFormationRecord.prop``
    """

    url: str
    type: str
    type_ng: str
    srv: str
    srv_ng: str
    res: str
    res_ng: str
    prop: T.Optional[str] = dataclasses.field(default=None)
    prop_ng: T.Optional[str] = dataclasses.field(default=None)

    @property
    def title(self) -> str:
        if self.prop_ng:
            return f"{self.type_ng}: {self.srv_ng} | {self.res_ng} - {self.prop_ng}"
        else:
            return f"{self.type_ng}: {self.srv_ng} | {self.res_ng}"


aws_cloudformation_fields = [
    sayt.StoredField(
        name="url",
    ),
    sayt.TextField(
        name="type",
        stored=True,
        field_boost=10.0,
    ),
    sayt.NgramWordsField(
        name="type_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=10.0,
    ),
    sayt.TextField(
        name="srv",
        stored=True,
        field_boost=5.0,
    ),
    sayt.NgramWordsField(
        name="srv_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=5.0,
    ),
    sayt.TextField(
        name="res",
        stored=True,
        field_boost=10.0,
    ),
    sayt.NgramWordsField(
        name="res_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=10.0,
    ),
    sayt.TextField(
        name="prop",
        stored=True,
        field_boost=10.0,
    ),
    sayt.NgramWordsField(
        name="prop_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=10.0,
    ),
]


# ------------------------------------------------------------------------------
# AWS Python SDK - boto3
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class Boto3AwsService(BaseModel):
    """
    AWS Service data model.

    :param name: it is the clickable text in the boto3 document homepage sidebar.
        For example, for Identity Access Management, the url is
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html,
        the clickable text in the sidebar is "IAM".
    :param doc_url: the boto3 document url, for example, the IAM document url is
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html
    """

    name: str = dataclasses.field()
    doc_url: str = dataclasses.field()


@dataclasses.dataclass
class Boto3Record(BaseRecord):
    """
        Example: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/create_role.html

    :param url: in this example, it is
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/create_role.html
        :param type: ``"client"`` or ``"pagi"``,
            ``"client"`` means it is a client method,
            ``"pagi"`` means it is a paginator method.
            in this example, it is ``"client"``.
        :param service_id: in this example, it is the ``"iam"``, the argument for ``boto3.client("iam")``.
        :param service_name: in this example, "IAM" is the text on the document page sidebar
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html
        :param method: in this example, it is the method name ``"create_role"``.
    """

    url: str
    type: str
    service_id: str
    service_name: str
    method: str

    @property
    def sort_key(self) -> str:
        return " ".join([self.service_id, self.type, self.method])

    def to_doc(self) -> "Boto3Document":
        return Boto3Document(
            url=self.url,
            type=self.type,
            srv=tokenify(self.service_name),
            srv_ng=self.service_name,
            srv_id=tokenify(self.service_id),
            srv_id_ng=self.service_id,
            meth=tokenify(self.method),
            meth_ng=self.method,
        )


@dataclasses.dataclass
class Boto3Document(CommonDocument):
    """
    Example: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/create_role.html

    :param url: same as :attr:`Boto3Record.url`
    :param type: same as :attr:`Boto3Record.type`
    :param srv: same as :attr:`Boto3Record.service_name`
    :param srv_ng: same as :attr:`Boto3Record.service_name`
    :param srv_id: same as :attr:`Boto3Record.service_id`
    :param srv_id_ng: same as :attr:`Boto3Record.service_id`
    :param meth: same as :attr:`Boto3Record.method`
    :param meth_ng: same as :attr:`Boto3Record.method`
    """

    url: str
    type: str
    srv: str
    srv_ng: str
    srv_id: str
    srv_id_ng: str
    meth: str
    meth_ng: str

    @property
    def title(self) -> str:
        return f"{self.type} | {self.srv_id_ng.lower()}.{self.meth_ng}"


boto3_fields = [
    sayt.StoredField(
        name="url",
    ),
    sayt.KeywordField(
        name="type",
        stored=True,
        field_boost=10.0,
    ),
    sayt.TextField(
        name="srv",
        stored=True,
        field_boost=5.0,
    ),
    sayt.NgramWordsField(
        name="srv_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=5.0,
    ),
    sayt.TextField(
        name="srv_id",
        stored=True,
        field_boost=5.0,
    ),
    sayt.NgramWordsField(
        name="srv_id_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=5.0,
    ),
    sayt.TextField(
        name="meth",
        stored=True,
    ),
    sayt.NgramWordsField(
        name="meth_ng",
        stored=True,
        minsize=2,
        maxsize=6,
    ),
]


# ------------------------------------------------------------------------------
# AWS CDK Python
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class CdkPythonService:
    """
    Example: https://docs.aws.amazon.com/cdk/api/v2/python/modules.html

    :param service: the service name in the text on the left hand side menu,
        in this example, it is ``"aws_cdk.aws_s3"``
    :param url: the url
    """

    name: str
    url: str

    @property
    def short_name(self) -> str:
        """
        ``"s3"``, it is from the ``"aws_cdk.aws_s3"``
        """
        return self.name.replace("aws_cdk.aws_", "").replace("aws_cdk.", "")


@dataclasses.dataclass
class CdkPythonRecord(BaseRecord):
    """
        Example: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html

    :param url: the url of the object in the per-service package overview
        In this example, it is https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html
    :param service: the service name in the text on the left hand side menu on
        https://docs.aws.amazon.com/cdk/api/v2/python/modules.html
        In this example, it is ``"s3"``, it is from the ``aws_cdk.aws_s3``,
        with ``aws_cdk.aws_`` stripped off.
    :param object: the object name in the text in the per-service package overview
        page table on https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3.html,
        In this example, it is ``"Bucket"``.
    """

    url: str
    service: str
    object: str

    @property
    def sort_key(self) -> str:
        return " ".join([self.service, self.object])

    def to_doc(self) -> "CdkPythonDocument":
        return CdkPythonDocument(
            url=self.url,
            srv=tokenify(self.service),
            srv_ng=self.service,
            obj=tokenify(self.object),
            obj_ng=self.object,
        )


@dataclasses.dataclass
class CdkPythonDocument(CommonDocument):
    """
    Example: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html

    :param url: same as :attr:`CdkPythonRecord.url``
    :param srv: same as :attr:`CdkPythonRecord.service``
    :param srv_ng: same as :attr:`CdkPythonRecord.service``
    :param obj: same as :attr:`CdkPythonRecord.object``
    :param obj_ng: same as :attr:`CdkPythonRecord.object``
    """

    url: str
    srv: str
    srv_ng: str
    obj: str
    obj_ng: str

    @property
    def title(self) -> str:
        return f"{self.srv_ng} | {self.obj_ng}"


cdk_python_fields = [
    sayt.StoredField(
        name="url",
    ),
    sayt.TextField(
        name="srv",
        stored=True,
        field_boost=5.0,
    ),
    sayt.NgramWordsField(
        name="srv_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=5.0,
    ),
    sayt.TextField(
        name="obj",
        stored=True,
    ),
    sayt.NgramWordsField(
        name="obj_ng",
        stored=True,
        minsize=2,
        maxsize=6,
    ),
]


# ------------------------------------------------------------------------------
# AWS CDK TypeScript
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class CdkTypeScriptRecord(BaseRecord):
    """
    Example: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html

    :param url: the url of the object in the per-service package overview
            In this example, it is https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html
        :param service: the service name in the text on the left hand side menu on
            https://docs.aws.amazon.com/cdk/api/v2/python/modules.html
            In this example, it is ``"s3"``, it is from the ``aws_cdk.aws_s3``,
            with ``aws_cdk.aws_`` stripped off.
        :param object: the object name in the text in the per-service package overview
            page table on https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3.html,
            In this example, it is ``"Bucket"``.
    """

    url: str
    service_name: str
    resource_type: str
    resource_name: str

    @property
    def sort_key(self) -> str:
        return " ".join([self.service_name, self.resource_type, self.resource_name])

    def to_doc(self) -> "CdkTypeScriptDocument":
        return CdkTypeScriptDocument(
            url=self.url,
            srv=tokenify(self.service_name),
            srv_ng=self.service_name,
            res_type=tokenify(self.resource_type),
            res_type_ng=self.resource_type,
            res_name=tokenify(self.resource_name),
            res_name_ng=self.resource_name,
        )


@dataclasses.dataclass
class CdkTypeScriptDocument(CommonDocument):
    """
    Example: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html

    :param url: same as :attr:`CdkTypeScriptRecord.url``
    :param srv: same as :attr:`CdkTypeScriptRecord.service_name``
    :param srv_ng: same as :attr:`CdkTypeScriptRecord.service_name``
    :param res_type: same as :attr:`CdkTypeScriptRecord.resource_type``
    :param res_type_ng: same as :attr:`CdkTypeScriptRecord.resource_type``
    :param res_name: same as :attr:`CdkTypeScriptRecord.resource_name``
    :param res_name_ng: same as :attr:`CdkTypeScriptRecord.resource_name``
    """

    url: str
    srv: str
    srv_ng: str
    res_type: str
    res_type_ng: str
    res_name: str
    res_name_ng: str

    @property
    def title(self) -> str:
        return f"{self.srv_ng} | {self.res_type_ng} - {self.res_name_ng}"


cdk_ts_fields = [
    sayt.StoredField(
        name="url",
    ),
    sayt.TextField(
        name="srv",
        stored=True,
        field_boost=5.0,
    ),
    sayt.NgramWordsField(
        name="srv_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=5.0,
    ),
    sayt.TextField(
        name="res_type",
        stored=True,
        field_boost=10.0,
    ),
    sayt.NgramWordsField(
        name="res_type_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=10.0,
    ),
    sayt.TextField(
        name="res_name",
        stored=True,
        field_boost=5.0,
    ),
    sayt.NgramWordsField(
        name="res_name_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=5.0,
    ),
]


# ------------------------------------------------------------------------------
# PySpark
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class PySparkRecord(BaseRecord):
    """
    Example: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.html

    :param header1: the header1 of the text in the side menu, in this example,
        it is ``"Spark SQL"``.
    :param header2: the header2 of the text in the side menu, in this example,
        it is ``"Core Classes"``.
    :param header3: the header3 of the text in the side menu, in this example,
        it is ``"sql.SparkSession"``. We strip off the ``"pyspark."`` part.
    """

    url: str
    header1: str
    header2: T.Optional[str]
    header3: T.Optional[str]

    @property
    def sort_key(self) -> str:
        return " ".join([self.header1, str(self.header2), str(self.header3)])

    def to_doc(self) -> "PySparkDocument":
        return PySparkDocument(
            h1=self.header1,
            h1_ng=self.header1,
            h2=tokenify(self.header2) if self.header2 else None,
            h2_ng=self.header2,
            h3=tokenify(self.header3) if self.header3 else None,
            h3_ng=self.header3,
            url=self.url,
        )


@dataclasses.dataclass
class PySparkDocument(CommonDocument):
    """
    Example: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.html

    :param url: same as :attr:`PySparkRecord.url``
    :param h1: same as :attr:`PySparkRecord.header1``
    :param h1_ng: same as :attr:`PySparkRecord.header1``
    :param h2: same as :attr:`PySparkRecord.header2``
    :param h2_ng: same as :attr:`PySparkRecord.header2``
    :param h3: same as :attr:`PySparkRecord.header3``
    :param h3_ng: same as :attr:`PySparkRecord.header3``
    """

    url: str
    h1: str
    h1_ng: str
    h2: T.Optional[str] = dataclasses.field(default=None)
    h2_ng: T.Optional[str] = dataclasses.field(default=None)
    h3: T.Optional[str] = dataclasses.field(default=None)
    h3_ng: T.Optional[str] = dataclasses.field(default=None)

    @property
    def title(self) -> str:
        parts = [self.h1_ng]
        if self.h2_ng:
            parts.append(self.h2_ng)
        if self.h3_ng:
            parts.append(self.h3_ng)
        return " | ".join(parts)


pyspark_fields = [
    sayt.StoredField(
        name="url",
    ),
    sayt.TextField(
        name="h1",
        stored=True,
    ),
    sayt.NgramWordsField(
        name="h1_ng",
        stored=True,
        minsize=2,
        maxsize=6,
    ),
    sayt.TextField(
        name="h2",
        stored=True,
        field_boost=5.0,
    ),
    sayt.NgramWordsField(
        name="h2_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=5.0,
    ),
    sayt.TextField(
        name="h3",
        stored=True,
        field_boost=10.0,
    ),
    sayt.NgramWordsField(
        name="h3_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=10.0,
    ),
]


# ------------------------------------------------------------------------------
# Pandas
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class PandasRecord(BaseRecord):
    """
    Example: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

    :param header1: the header1 of the text in the side menu, in this example,
        it is ``"Input/output"``.
    :param header2: the header2 of the API method in the side menu, but with
        "pandas." prefix removed, in this example, it is ``"read_csv"``.
    """

    url: str
    header1: str
    header2: T.Optional[str]

    @property
    def sort_key(self) -> str:
        return " ".join([self.header1, str(self.header2)])

    def to_doc(self) -> "PandasDocument":
        return PandasDocument(
            h1=self.header1,
            h1_ng=self.header1,
            h2=tokenify(self.header2) if self.header2 else None,
            h2_ng=self.header2,
            url=self.url,
        )


@dataclasses.dataclass
class PandasDocument(CommonDocument):
    """
    Example: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

    :param url: same as :attr:`PandasRecord.url``
    :param h1: same as :attr:`PandasRecord.header1``
    :param h1_ng: same as :attr:`PandasRecord.header1``
    :param h2: same as :attr:`PandasRecord.header2``
    :param h2_ng: same as :attr:`PandasRecord.header2``
    """

    url: str
    h1: str
    h1_ng: str
    h2: T.Optional[str] = dataclasses.field(default=None)
    h2_ng: T.Optional[str] = dataclasses.field(default=None)

    @property
    def title(self) -> str:
        parts = [self.h1_ng]
        if self.h2_ng:
            parts.append(self.h2_ng)
        return " | ".join(parts)


pandas_fields = [
    sayt.StoredField(
        name="url",
    ),
    sayt.TextField(
        name="h1",
        stored=True,
    ),
    sayt.NgramWordsField(
        name="h1_ng",
        stored=True,
        minsize=2,
        maxsize=6,
    ),
    sayt.TextField(
        name="h2",
        stored=True,
        field_boost=5.0,
    ),
    sayt.NgramWordsField(
        name="h2_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=5.0,
    ),
]


# ------------------------------------------------------------------------------
# Terraform
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class TfProvider(BaseModel):
    """
    Example:

    - Terraform provider: https://registry.terraform.io/providers/hashicorp/aws/latest
    - Git repo: https://github.com/hashicorp/terraform-provider-aws

    List of hashicorp providers: https://registry.terraform.io/search/providers?namespace=hashicorp

    Click on the provider, then you can find the document source repo near "Source Code" section.

    :param provider_name: in this example, it is ``"aws"``, the url part in the
        terraform provider url.
    :param provider_short_name: provider short name for search, in example, it is ``"AWS"``
    :param github_repo_name: the github repo name, in example, it is ``"terraform-provider-aws"``
    """

    provider_name: str
    provider_short_name: str
    github_repo_name: str


TF_PROVIDERS = [
    TfProvider(
        provider_name="aws",
        provider_short_name="AWS",
        github_repo_name="terraform-provider-aws",
    ),
    TfProvider(
        provider_name="azurerm",
        provider_short_name="AZ",
        github_repo_name="terraform-provider-azurerm",
    ),
    TfProvider(
        provider_name="google",
        provider_short_name="GCP",
        github_repo_name="terraform-provider-google",
    ),
]

tf_provider_short_name_to_provider_name_mapper = {
    provider.provider_short_name: provider.provider_name for provider in TF_PROVIDERS
}


@dataclasses.dataclass
class TfItemType(BaseModel):
    """
    Example:

    - web page: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance
    - source doc: https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/instance.html.markdown

    :param item_type: "Res" or "DS", in this example, it is ``"Res"``
    :param folder_name: the folder name in the source doc, in this example, it is ``"r"``
    :param url_key: the url part in the web page url, in this example, it is ``"resources"``
    """

    item_type: str
    folder_name: str
    url_key: str


TF_ITEM_TYPES = [
    TfItemType(
        item_type="Res",
        folder_name="r",
        url_key="resources",
    ),
    TfItemType(
        item_type="DS",
        folder_name="d",
        url_key="data-sources",
    ),
]

tf_item_type_to_url_key_mapper = {
    item_type.item_type: item_type.url_key for item_type in TF_ITEM_TYPES
}


@dataclasses.dataclass
class TfRecord(BaseRecord):
    """
        Example:

        - webpage: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance
        - source doc: https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/instance.html.markdown

    :param url: in this example, it is
            https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance
        :param provider: provider short name, in this example, it is ``"aws"``.
        :param type: ``"res"`` (resource) or ``"ds"`` (dataset), in this example,
            it is ``"res"``.
        :param subcategory: the subcategory in the markdown metadata,
            in this example, it is ``"EC2 (Elastic Compute Cloud)"``.
        :param page_title: the subcategory in the markdown metadata,
            in this example, it is ``"AWS: aws_instance"``.
        :param description: the description in the markdown metadata,
            in this example, it is ``"Provides an EC2 instance resource. This allows instances to be created, updated, and deleted. Instances also support provisioning."``.
    """

    url: str
    provider: str
    type: str
    subcategory: str
    item_name: str
    description: str

    @property
    def sort_key(self) -> str:
        return " ".join([self.provider, self.type, self.subcategory, self.item_name])

    def to_doc(self) -> "TfDocument":
        return TfDocument(
            url=self.url,
            provider=self.provider,
            type=self.type,
            cate=tokenify(self.subcategory),
            cate_ng=self.subcategory,
            item=tokenify(self.item_name),
            item_ng=self.item_name,
            desc=self.description,
        )


@dataclasses.dataclass
class TfDocument(CommonDocument):
    """
    Example:

    - webpage: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance
    - source doc: https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/instance.html.markdown

    :param url: same as :attr:`TfRecord.url``
    :param provider: same as :attr:`TfRecord.provider``
    :param type: same as :attr:`TfRecord.type``
    :param cate: same as :attr:`TfRecord.subcategory``
    :param cate_ng: same as :attr:`TfRecord.subcategory``
    :param item: same as :attr:`TfRecord.item_name``
    :param item_ng: same as :attr:`TfRecord.item_name``
    :param desc: same as :attr:`TfRecord.description``
    """

    url: str
    provider: str
    type: str
    cate: str
    cate_ng: str
    item: str
    item_ng: str
    desc: str

    @property
    def title(self) -> str:
        return f"{self.provider} {self.type}: {self.cate_ng} | {self.item_ng}"


tf_fields = [
    sayt.StoredField(
        name="url",
    ),
    sayt.KeywordField(
        name="provider",
        stored=True,
        lowercase=True,
        field_boost=10.0,
    ),
    sayt.KeywordField(
        name="type",
        stored=True,
        lowercase=True,
        field_boost=5.0,
    ),
    sayt.TextField(
        name="cate",
        stored=True,
        field_boost=2.0,
    ),
    sayt.NgramWordsField(
        name="cate_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=2.0,
    ),
    sayt.TextField(
        name="item",
        stored=True,
    ),
    sayt.NgramWordsField(
        name="item_ng",
        stored=True,
        minsize=2,
        maxsize=6,
    ),
    sayt.StoredField(
        name="desc",
    ),
]

# ==============================================================================
# Download data
# ==============================================================================
# NOTE: don't forget to update this mapper when you add a new dataset
_dataset_mapper = {
    DataSetEnum.airflow.value: {
        "doc_class": AirflowDocument,
        "fields": airflow_fields,
    },
    DataSetEnum.aws_cloudformation.value: {
        "doc_class": AwsCloudFormationDocument,
        "fields": aws_cloudformation_fields,
    },
    DataSetEnum.boto3.value: {
        "doc_class": Boto3Document,
        "fields": boto3_fields,
    },
    DataSetEnum.cdk_python.value: {
        "doc_class": CdkPythonDocument,
        "fields": cdk_python_fields,
    },
    DataSetEnum.cdk_ts.value: {
        "doc_class": CdkTypeScriptDocument,
        "fields": cdk_ts_fields,
    },
    DataSetEnum.pyspark.value: {
        "doc_class": PySparkDocument,
        "fields": pyspark_fields,
    },
    DataSetEnum.pandas.value: {
        "doc_class": PandasDocument,
        "fields": pandas_fields,
    },
    DataSetEnum.tf.value: {
        "doc_class": TfDocument,
        "fields": tf_fields,
    },
}


def get_doc_class(
    dataset: str,
) -> T.Type[
    T.Union[
        AirflowDocument,
        Boto3Document,
        CdkPythonDocument,
        CdkTypeScriptDocument,
        PySparkDocument,
        TfDocument,
    ]
]:
    """
    Get the document class for the given dataset.
    """
    return _dataset_mapper[dataset]["doc_class"]


def get_fields(dataset: str) -> T.List[sayt.T_Field]:
    """
    Get the list of ``sayt.Field`` object for the given dataset.
    """
    return _dataset_mapper[dataset]["fields"]


def http_get(url) -> str:
    """
    Similar to ``requests.get``.
    """
    with request.urlopen(url) as response:
        return response.read().decode("utf-8").strip()


def get_dataset_data(dataset: str) -> T.List[sayt.T_DOCUMENT]:
    """
    Download the latest dataset data from GitHub release.
    """
    gh_api_url = (
        "https://api.github.com/repos/MacHu-GWU/findref-project/releases/latest"
    )
    tag_name = json.loads(http_get(gh_api_url))["tag_name"]
    url = f"https://github.com/MacHu-GWU/findref-project/releases/download/{tag_name}/{dataset}-LATEST.json"
    return json.loads(http_get(url))["docs"]


def create_sayt_dataset(
    dataset: str,
    dir_index: Path,
    dir_cache: Path,
) -> sayt.DataSet:
    """
    Create a ``sayt.DataSet`` object for the given dataset.
    """

    def downloader():
        return get_dataset_data(dataset)

    return sayt.DataSet(
        dir_index=dir_index,
        index_name=f"findref-{dataset}",
        fields=get_fields(dataset),
        dir_cache=dir_cache,
        cache_key=f"findref-{dataset}",
        cache_tag=f"findref-{dataset}",
        cache_expire=30 * 24 * 60 * 60,
        downloader=downloader,
    )
