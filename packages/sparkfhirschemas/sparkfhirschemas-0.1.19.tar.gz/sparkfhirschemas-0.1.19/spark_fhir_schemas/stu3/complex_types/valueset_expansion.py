from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import DataType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class ValueSet_ExpansionSchema:
    """
    A value set specifies a set of codes drawn from one or more code systems.
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
        A value set specifies a set of codes drawn from one or more code systems.


        identifier: An identifier that uniquely identifies this expansion of the valueset. Systems
            may re-use the same identifier as long as the expansion and the definition
            remain the same, but are not required to do so.

        timestamp: The time at which the expansion was produced by the expanding system.

        total: The total number of concepts in the expansion. If the number of concept nodes
            in this resource is less than the stated number, then the server can return
            more using the offset parameter.

        offset: If paging is being used, the offset at which this resource starts.  I.e. this
            resource is a partial view into the expansion. If paging is not being used,
            this element SHALL not be present.

        parameter: A parameter that controlled the expansion process. These parameters may be
            used by users of expanded value sets to check whether the expansion is
            suitable for a particular purpose, or to pick the correct expansion.

        contains: The codes that are contained in the value set expansion.

        """
        from spark_fhir_schemas.stu3.complex_types.valueset_parameter import ValueSet_ParameterSchema
        from spark_fhir_schemas.stu3.complex_types.valueset_contains import ValueSet_ContainsSchema
        if (
            max_recursion_limit
            and nesting_list.count("ValueSet_Expansion") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["ValueSet_Expansion"]
        schema = StructType(
            [
                # An identifier that uniquely identifies this expansion of the valueset. Systems
                # may re-use the same identifier as long as the expansion and the definition
                # remain the same, but are not required to do so.
                StructField("identifier", StringType(), True),
                # The time at which the expansion was produced by the expanding system.
                StructField("timestamp", StringType(), True),
                # The total number of concepts in the expansion. If the number of concept nodes
                # in this resource is less than the stated number, then the server can return
                # more using the offset parameter.
                StructField("total", IntegerType(), True),
                # If paging is being used, the offset at which this resource starts.  I.e. this
                # resource is a partial view into the expansion. If paging is not being used,
                # this element SHALL not be present.
                StructField("offset", IntegerType(), True),
                # A parameter that controlled the expansion process. These parameters may be
                # used by users of expanded value sets to check whether the expansion is
                # suitable for a particular purpose, or to pick the correct expansion.
                StructField(
                    "parameter",
                    ArrayType(
                        ValueSet_ParameterSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # The codes that are contained in the value set expansion.
                StructField(
                    "contains",
                    ArrayType(
                        ValueSet_ContainsSchema.get_schema(
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
