from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import BooleanType
from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class FamilyMemberHistory_ConditionSchema:
    """
    Significant health conditions for a person related to the patient relevant in
    the context of care for the patient.
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
        Significant health conditions for a person related to the patient relevant in
        the context of care for the patient.


        id: Unique id for the element within a resource (for internal references). This
            may be any string value that does not contain spaces.

        extension: May be used to represent additional information that is not part of the basic
            definition of the element. To make the use of extensions safe and manageable,
            there is a strict set of governance  applied to the definition and use of
            extensions. Though any implementer can define an extension, there is a set of
            requirements that SHALL be met as part of the definition of the extension.

        code: The actual condition specified. Could be a coded condition (like MI or
            Diabetes) or a less specific string like 'cancer' depending on how much is
            known about the condition and the capabilities of the creating system.

        outcome: Indicates what happened following the condition.  If the condition resulted in
            death, deceased date is captured on the relation.

        contributedToDeath: This condition contributed to the cause of death of the related person. If
            contributedToDeath is not populated, then it is unknown.

        onsetAge: Either the age of onset, range of approximate age or descriptive string can be
            recorded.  For conditions with multiple occurrences, this describes the first
            known occurrence.

        onsetRange: Either the age of onset, range of approximate age or descriptive string can be
            recorded.  For conditions with multiple occurrences, this describes the first
            known occurrence.

        onsetPeriod: Either the age of onset, range of approximate age or descriptive string can be
            recorded.  For conditions with multiple occurrences, this describes the first
            known occurrence.

        onsetString: Either the age of onset, range of approximate age or descriptive string can be
            recorded.  For conditions with multiple occurrences, this describes the first
            known occurrence.

        note: An area where general notes can be placed about this specific condition.

        """
        from spark_fhir_schemas.r4.complex_types.extension import ExtensionSchema
        from spark_fhir_schemas.r4.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.r4.complex_types.age import AgeSchema
        from spark_fhir_schemas.r4.complex_types.range import RangeSchema
        from spark_fhir_schemas.r4.complex_types.period import PeriodSchema
        from spark_fhir_schemas.r4.complex_types.annotation import AnnotationSchema
        if (
            max_recursion_limit
            and nesting_list.count("FamilyMemberHistory_Condition") >=
            max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + [
            "FamilyMemberHistory_Condition"
        ]
        schema = StructType(
            [
                # Unique id for the element within a resource (for internal references). This
                # may be any string value that does not contain spaces.
                StructField("id", StringType(), True),
                # May be used to represent additional information that is not part of the basic
                # definition of the element. To make the use of extensions safe and manageable,
                # there is a strict set of governance  applied to the definition and use of
                # extensions. Though any implementer can define an extension, there is a set of
                # requirements that SHALL be met as part of the definition of the extension.
                StructField(
                    "extension",
                    ArrayType(
                        ExtensionSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # The actual condition specified. Could be a coded condition (like MI or
                # Diabetes) or a less specific string like 'cancer' depending on how much is
                # known about the condition and the capabilities of the creating system.
                StructField(
                    "code",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Indicates what happened following the condition.  If the condition resulted in
                # death, deceased date is captured on the relation.
                StructField(
                    "outcome",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # This condition contributed to the cause of death of the related person. If
                # contributedToDeath is not populated, then it is unknown.
                StructField("contributedToDeath", BooleanType(), True),
                # Either the age of onset, range of approximate age or descriptive string can be
                # recorded.  For conditions with multiple occurrences, this describes the first
                # known occurrence.
                StructField(
                    "onsetAge",
                    AgeSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Either the age of onset, range of approximate age or descriptive string can be
                # recorded.  For conditions with multiple occurrences, this describes the first
                # known occurrence.
                StructField(
                    "onsetRange",
                    RangeSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Either the age of onset, range of approximate age or descriptive string can be
                # recorded.  For conditions with multiple occurrences, this describes the first
                # known occurrence.
                StructField(
                    "onsetPeriod",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Either the age of onset, range of approximate age or descriptive string can be
                # recorded.  For conditions with multiple occurrences, this describes the first
                # known occurrence.
                StructField("onsetString", StringType(), True),
                # An area where general notes can be placed about this specific condition.
                StructField(
                    "note",
                    ArrayType(
                        AnnotationSchema.get_schema(
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
