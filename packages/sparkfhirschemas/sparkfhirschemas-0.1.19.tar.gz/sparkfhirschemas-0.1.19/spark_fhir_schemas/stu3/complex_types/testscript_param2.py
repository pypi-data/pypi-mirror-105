from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class TestScript_Param2Schema:
    """
    A structured set of tests against a FHIR server implementation to determine
    compliance against the FHIR specification.
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
        A structured set of tests against a FHIR server implementation to determine
        compliance against the FHIR specification.


        name: Descriptive name for this parameter that matches the external assert rule
            parameter name.

        value: The value for the parameter that will be passed on to the external rule
            template.

        """
        if (
            max_recursion_limit
            and nesting_list.count("TestScript_Param2") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["TestScript_Param2"]
        schema = StructType(
            [
                # Descriptive name for this parameter that matches the external assert rule
                # parameter name.
                StructField("name", StringType(), True),
                # The value for the parameter that will be passed on to the external rule
                # template.
                StructField("value", StringType(), True),
            ]
        )
        if not include_extension:
            schema.fields = [
                c if c.name != "extension" else
                StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
