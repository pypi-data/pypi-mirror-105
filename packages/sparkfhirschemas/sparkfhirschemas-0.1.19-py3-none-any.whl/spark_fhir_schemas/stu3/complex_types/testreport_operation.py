from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class TestReport_OperationSchema:
    """
    A summary of information based on the results of executing a TestScript.
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
        A summary of information based on the results of executing a TestScript.


        result: The result of this operation.

        message: An explanatory message associated with the result.

        detail: A link to further details on the result.

        """
        if (
            max_recursion_limit and
            nesting_list.count("TestReport_Operation") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["TestReport_Operation"]
        schema = StructType(
            [
                # The result of this operation.
                StructField("result", StringType(), True),
                # An explanatory message associated with the result.
                StructField("message", StringType(), True),
                # A link to further details on the result.
                StructField("detail", StringType(), True),
            ]
        )
        if not include_extension:
            schema.fields = [
                c if c.name != "extension" else
                StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
