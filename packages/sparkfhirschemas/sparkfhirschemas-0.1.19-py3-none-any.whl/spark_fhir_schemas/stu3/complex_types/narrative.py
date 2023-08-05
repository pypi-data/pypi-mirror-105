from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class NarrativeSchema:
    """
    A human-readable formatted text, including images.
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
        A human-readable formatted text, including images.


        status: The status of the narrative - whether it's entirely generated (from just the
            defined data or the extensions too), or whether a human authored it and it may
            contain additional data.

        div: The actual narrative content, a stripped down version of XHTML.

        """
        if (
            max_recursion_limit
            and nesting_list.count("Narrative") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Narrative"]
        schema = StructType(
            [
                # The status of the narrative - whether it's entirely generated (from just the
                # defined data or the extensions too), or whether a human authored it and it may
                # contain additional data.
                StructField("status", StringType(), True),
                # The actual narrative content, a stripped down version of XHTML.
                StructField("div", StringType(), True),
            ]
        )
        if not include_extension:
            schema.fields = [
                c if c.name != "extension" else
                StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
