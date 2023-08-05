from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import BooleanType
from pyspark.sql.types import DataType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class Parameters_ParameterSchema:
    """
    This special resource type is used to represent an operation request and
    response (operations.html). It has no other use, and there is no RESTful
    endpoint associated with it.
    """
    # noinspection PyDefaultArgument
    @staticmethod
    def get_schema(
        max_nesting_depth: Optional[int] = 6,
        nesting_depth: int = 0,
        nesting_list: List[str] = [],
        max_recursion_limit: Optional[int] = 2,
        include_extension: Optional[bool] = False
    ) -> Union[StructType, DataType]:
        """
        This special resource type is used to represent an operation request and
        response (operations.html). It has no other use, and there is no RESTful
        endpoint associated with it.


        name: The name of the parameter (reference to the operation definition).

        valueBoolean: If the parameter is a data type.

        valueInteger: If the parameter is a data type.

        valueDecimal: If the parameter is a data type.

        valueBase64Binary: If the parameter is a data type.

        valueInstant: If the parameter is a data type.

        valueString: If the parameter is a data type.

        valueUri: If the parameter is a data type.

        valueDate: If the parameter is a data type.

        valueDateTime: If the parameter is a data type.

        valueTime: If the parameter is a data type.

        valueCode: If the parameter is a data type.

        valueOid: If the parameter is a data type.

        valueUuid: If the parameter is a data type.

        valueId: If the parameter is a data type.

        valueUnsignedInt: If the parameter is a data type.

        valuePositiveInt: If the parameter is a data type.

        valueMarkdown: If the parameter is a data type.

        valueElement: If the parameter is a data type.

        valueExtension: If the parameter is a data type.

        valueBackboneElement: If the parameter is a data type.

        valueNarrative: If the parameter is a data type.

        valueAnnotation: If the parameter is a data type.

        valueAttachment: If the parameter is a data type.

        valueIdentifier: If the parameter is a data type.

        valueCodeableConcept: If the parameter is a data type.

        valueCoding: If the parameter is a data type.

        valueQuantity: If the parameter is a data type.

        valueDuration: If the parameter is a data type.

        valueSimpleQuantity: If the parameter is a data type.

        valueDistance: If the parameter is a data type.

        valueCount: If the parameter is a data type.

        valueMoney: If the parameter is a data type.

        valueAge: If the parameter is a data type.

        valueRange: If the parameter is a data type.

        valuePeriod: If the parameter is a data type.

        valueRatio: If the parameter is a data type.

        valueReference: If the parameter is a data type.

        valueSampledData: If the parameter is a data type.

        valueSignature: If the parameter is a data type.

        valueHumanName: If the parameter is a data type.

        valueAddress: If the parameter is a data type.

        valueContactPoint: If the parameter is a data type.

        valueTiming: If the parameter is a data type.

        valueMeta: If the parameter is a data type.

        valueElementDefinition: If the parameter is a data type.

        valueContactDetail: If the parameter is a data type.

        valueContributor: If the parameter is a data type.

        valueDosage: If the parameter is a data type.

        valueRelatedArtifact: If the parameter is a data type.

        valueUsageContext: If the parameter is a data type.

        valueDataRequirement: If the parameter is a data type.

        valueParameterDefinition: If the parameter is a data type.

        valueTriggerDefinition: If the parameter is a data type.

        resource: If the parameter is a whole resource.

        part: A named part of a multi-part parameter.

        """
        from spark_fhir_schemas.stu3.complex_types.element import ElementSchema
        from spark_fhir_schemas.stu3.complex_types.extension import ExtensionSchema
        from spark_fhir_schemas.stu3.complex_types.backboneelement import BackboneElementSchema
        from spark_fhir_schemas.stu3.complex_types.narrative import NarrativeSchema
        from spark_fhir_schemas.stu3.complex_types.annotation import AnnotationSchema
        from spark_fhir_schemas.stu3.complex_types.attachment import AttachmentSchema
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.stu3.complex_types.coding import CodingSchema
        from spark_fhir_schemas.stu3.complex_types.quantity import QuantitySchema
        from spark_fhir_schemas.stu3.complex_types.duration import DurationSchema
        from spark_fhir_schemas.stu3.complex_types.distance import DistanceSchema
        from spark_fhir_schemas.stu3.complex_types.count import CountSchema
        from spark_fhir_schemas.stu3.complex_types.money import MoneySchema
        from spark_fhir_schemas.stu3.complex_types.age import AgeSchema
        from spark_fhir_schemas.stu3.complex_types.range import RangeSchema
        from spark_fhir_schemas.stu3.complex_types.period import PeriodSchema
        from spark_fhir_schemas.stu3.complex_types.ratio import RatioSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.sampleddata import SampledDataSchema
        from spark_fhir_schemas.stu3.complex_types.signature import SignatureSchema
        from spark_fhir_schemas.stu3.complex_types.humanname import HumanNameSchema
        from spark_fhir_schemas.stu3.complex_types.address import AddressSchema
        from spark_fhir_schemas.stu3.complex_types.contactpoint import ContactPointSchema
        from spark_fhir_schemas.stu3.complex_types.timing import TimingSchema
        from spark_fhir_schemas.stu3.complex_types.meta import MetaSchema
        from spark_fhir_schemas.stu3.complex_types.elementdefinition import ElementDefinitionSchema
        from spark_fhir_schemas.stu3.complex_types.contactdetail import ContactDetailSchema
        from spark_fhir_schemas.stu3.complex_types.contributor import ContributorSchema
        from spark_fhir_schemas.stu3.complex_types.dosage import DosageSchema
        from spark_fhir_schemas.stu3.complex_types.relatedartifact import RelatedArtifactSchema
        from spark_fhir_schemas.stu3.complex_types.usagecontext import UsageContextSchema
        from spark_fhir_schemas.stu3.complex_types.datarequirement import DataRequirementSchema
        from spark_fhir_schemas.stu3.complex_types.parameterdefinition import ParameterDefinitionSchema
        from spark_fhir_schemas.stu3.complex_types.triggerdefinition import TriggerDefinitionSchema
        from spark_fhir_schemas.stu3.simple_types.resourcelist import ResourceListSchema
        if (
            max_recursion_limit and
            nesting_list.count("Parameters_Parameter") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Parameters_Parameter"]
        schema = StructType(
            [
                # The name of the parameter (reference to the operation definition).
                StructField("name", StringType(), True),
                # If the parameter is a data type.
                StructField("valueBoolean", BooleanType(), True),
                # If the parameter is a data type.
                StructField("valueInteger", IntegerType(), True),
                # If the parameter is a data type.
                StructField("valueDecimal", IntegerType(), True),
                # If the parameter is a data type.
                StructField("valueBase64Binary", StringType(), True),
                # If the parameter is a data type.
                StructField("valueInstant", StringType(), True),
                # If the parameter is a data type.
                StructField("valueString", StringType(), True),
                # If the parameter is a data type.
                StructField("valueUri", StringType(), True),
                # If the parameter is a data type.
                StructField("valueDate", StringType(), True),
                # If the parameter is a data type.
                StructField("valueDateTime", StringType(), True),
                # If the parameter is a data type.
                StructField("valueTime", StringType(), True),
                # If the parameter is a data type.
                StructField("valueCode", StringType(), True),
                # If the parameter is a data type.
                StructField("valueOid", StringType(), True),
                # If the parameter is a data type.
                StructField("valueUuid", StringType(), True),
                # If the parameter is a data type.
                StructField("valueId", StringType(), True),
                # If the parameter is a data type.
                StructField("valueUnsignedInt", IntegerType(), True),
                # If the parameter is a data type.
                StructField("valuePositiveInt", IntegerType(), True),
                # If the parameter is a data type.
                StructField("valueMarkdown", StringType(), True),
                # If the parameter is a data type.
                StructField(
                    "valueElement",
                    ElementSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueExtension",
                    ExtensionSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueBackboneElement",
                    BackboneElementSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueNarrative",
                    NarrativeSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueAnnotation",
                    AnnotationSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueAttachment",
                    AttachmentSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueIdentifier",
                    IdentifierSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueCodeableConcept",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueCoding",
                    CodingSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueQuantity",
                    QuantitySchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueDuration",
                    DurationSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueSimpleQuantity",
                    QuantitySchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueDistance",
                    DistanceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueCount",
                    CountSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueMoney",
                    MoneySchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueAge",
                    AgeSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueRange",
                    RangeSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valuePeriod",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueRatio",
                    RatioSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueReference",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueSampledData",
                    SampledDataSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueSignature",
                    SignatureSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueHumanName",
                    HumanNameSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueAddress",
                    AddressSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueContactPoint",
                    ContactPointSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueTiming",
                    TimingSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueMeta",
                    MetaSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueElementDefinition",
                    ElementDefinitionSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueContactDetail",
                    ContactDetailSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueContributor",
                    ContributorSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueDosage",
                    DosageSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueRelatedArtifact",
                    RelatedArtifactSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueUsageContext",
                    UsageContextSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueDataRequirement",
                    DataRequirementSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueParameterDefinition",
                    ParameterDefinitionSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a data type.
                StructField(
                    "valueTriggerDefinition",
                    TriggerDefinitionSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the parameter is a whole resource.
                StructField(
                    "resource",
                    ResourceListSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A named part of a multi-part parameter.
                StructField(
                    "part",
                    ArrayType(
                        Parameters_ParameterSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
            ]
        )
        if not include_extension:
            schema.fields = [
                c if c.name != "extension" else
                StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
