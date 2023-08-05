from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class PlanDefinition_ConditionSchema:
    """
    This resource allows for the definition of various types of plans as a
    sharable, consumable, and executable artifact. The resource is general enough
    to support the description of a broad range of clinical artifacts such as
    clinical decision support rules, order sets and protocols.
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
        This resource allows for the definition of various types of plans as a
        sharable, consumable, and executable artifact. The resource is general enough
        to support the description of a broad range of clinical artifacts such as
        clinical decision support rules, order sets and protocols.


        kind: The kind of condition.

        description: A brief, natural language description of the condition that effectively
            communicates the intended semantics.

        language: The media type of the language for the expression.

        expression: An expression that returns true or false, indicating whether or not the
            condition is satisfied.

        """
        if (
            max_recursion_limit
            and nesting_list.count("PlanDefinition_Condition") >=
            max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + [
            "PlanDefinition_Condition"
        ]
        schema = StructType(
            [
                # The kind of condition.
                StructField("kind", StringType(), True),
                # A brief, natural language description of the condition that effectively
                # communicates the intended semantics.
                StructField("description", StringType(), True),
                # The media type of the language for the expression.
                StructField("language", StringType(), True),
                # An expression that returns true or false, indicating whether or not the
                # condition is satisfied.
                StructField("expression", StringType(), True),
            ]
        )
        if not include_extension:
            schema.fields = [
                c if c.name != "extension" else
                StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
