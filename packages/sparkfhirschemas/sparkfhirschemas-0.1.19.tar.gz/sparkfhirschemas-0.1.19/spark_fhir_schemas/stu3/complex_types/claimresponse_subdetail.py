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
class ClaimResponse_SubDetailSchema:
    """
    This resource provides the adjudication details from the processing of a Claim
    resource.
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
        This resource provides the adjudication details from the processing of a Claim
        resource.


        sequenceLinkId: A service line number.

        noteNumber: A list of note references to the notes provided below.

        adjudication: The adjudications results.

        """
        from spark_fhir_schemas.stu3.complex_types.claimresponse_adjudication import ClaimResponse_AdjudicationSchema
        if (
            max_recursion_limit
            and nesting_list.count("ClaimResponse_SubDetail") >=
            max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["ClaimResponse_SubDetail"]
        schema = StructType(
            [
                # A service line number.
                StructField("sequenceLinkId", IntegerType(), True),
                # A list of note references to the notes provided below.
                # The adjudications results.
                StructField(
                    "adjudication",
                    ArrayType(
                        ClaimResponse_AdjudicationSchema.get_schema(
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
