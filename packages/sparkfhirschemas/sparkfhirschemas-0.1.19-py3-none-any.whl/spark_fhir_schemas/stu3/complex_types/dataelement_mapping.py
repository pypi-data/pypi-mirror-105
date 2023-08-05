from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class DataElement_MappingSchema:
    """
    The formal description of a single piece of information that can be gathered
    and reported.
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
        The formal description of a single piece of information that can be gathered
        and reported.


        identity: An internal id that is used to identify this mapping set when specific
            mappings are made on a per-element basis.

        uri: An absolute URI that identifies the specification that this mapping is
            expressed to.

        name: A name for the specification that is being mapped to.

        comment: Comments about this mapping, including version notes, issues, scope
            limitations, and other important notes for usage.

        """
        if (
            max_recursion_limit and
            nesting_list.count("DataElement_Mapping") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["DataElement_Mapping"]
        schema = StructType(
            [
                # An internal id that is used to identify this mapping set when specific
                # mappings are made on a per-element basis.
                StructField("identity", StringType(), True),
                # An absolute URI that identifies the specification that this mapping is
                # expressed to.
                StructField("uri", StringType(), True),
                # A name for the specification that is being mapped to.
                StructField("name", StringType(), True),
                # Comments about this mapping, including version notes, issues, scope
                # limitations, and other important notes for usage.
                StructField("comment", StringType(), True),
            ]
        )
        if not include_extension:
            schema.fields = [
                c if c.name != "extension" else
                StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
