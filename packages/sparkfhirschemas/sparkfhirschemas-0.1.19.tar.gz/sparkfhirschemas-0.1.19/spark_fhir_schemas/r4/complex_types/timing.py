from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class TimingSchema:
    """
    Specifies an event that may occur multiple times. Timing schedules are used to
    record when things are planned, expected or requested to occur. The most
    common usage is in dosage instructions for medications. They are also used
    when planning care of various kinds, and may be used for reporting the
    schedule to which past regular activities were carried out.
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
        Specifies an event that may occur multiple times. Timing schedules are used to
        record when things are planned, expected or requested to occur. The most
        common usage is in dosage instructions for medications. They are also used
        when planning care of various kinds, and may be used for reporting the
        schedule to which past regular activities were carried out.


        id: Unique id for the element within a resource (for internal references). This
            may be any string value that does not contain spaces.

        extension: May be used to represent additional information that is not part of the basic
            definition of the element. To make the use of extensions safe and manageable,
            there is a strict set of governance  applied to the definition and use of
            extensions. Though any implementer can define an extension, there is a set of
            requirements that SHALL be met as part of the definition of the extension.

        event: Identifies specific times when the event occurs.

        repeat: A set of rules that describe when the event is scheduled.

        code: A code for the timing schedule (or just text in code.text). Some codes such as
            BID are ubiquitous, but many institutions define their own additional codes.
            If a code is provided, the code is understood to be a complete statement of
            whatever is specified in the structured timing data, and either the code or
            the data may be used to interpret the Timing, with the exception that
            .repeat.bounds still applies over the code (and is not contained in the code).

        """
        from spark_fhir_schemas.r4.complex_types.extension import ExtensionSchema
        from spark_fhir_schemas.r4.simple_types.datetime import dateTimeSchema
        from spark_fhir_schemas.r4.complex_types.timing_repeat import Timing_RepeatSchema
        from spark_fhir_schemas.r4.complex_types.codeableconcept import CodeableConceptSchema
        if (
            max_recursion_limit
            and nesting_list.count("Timing") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Timing"]
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
                # Identifies specific times when the event occurs.
                StructField(
                    "event",
                    ArrayType(
                        dateTimeSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # A set of rules that describe when the event is scheduled.
                StructField(
                    "repeat",
                    Timing_RepeatSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A code for the timing schedule (or just text in code.text). Some codes such as
                # BID are ubiquitous, but many institutions define their own additional codes.
                # If a code is provided, the code is understood to be a complete statement of
                # whatever is specified in the structured timing data, and either the code or
                # the data may be used to interpret the Timing, with the exception that
                # .repeat.bounds still applies over the code (and is not contained in the code).
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
            ]
        )
        if not include_extension:
            schema.fields = [
                c if c.name != "extension" else
                StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
