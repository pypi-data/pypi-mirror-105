from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class CapabilityStatement_DocumentSchema:
    """
    A Capability Statement documents a set of capabilities (behaviors) of a FHIR
    Server that may be used as a statement of actual server functionality or a
    statement of required or desired server implementation.
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
        A Capability Statement documents a set of capabilities (behaviors) of a FHIR
        Server that may be used as a statement of actual server functionality or a
        statement of required or desired server implementation.


        mode: Mode of this document declaration - whether an application is a producer or
            consumer.

        documentation: A description of how the application supports or uses the specified document
            profile.  For example, when documents are created, what action is taken with
            consumed documents, etc.

        profile: A constraint on a resource used in the document.

        """
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        if (
            max_recursion_limit
            and nesting_list.count("CapabilityStatement_Document") >=
            max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + [
            "CapabilityStatement_Document"
        ]
        schema = StructType(
            [
                # Mode of this document declaration - whether an application is a producer or
                # consumer.
                StructField("mode", StringType(), True),
                # A description of how the application supports or uses the specified document
                # profile.  For example, when documents are created, what action is taken with
                # consumed documents, etc.
                StructField("documentation", StringType(), True),
                # A constraint on a resource used in the document.
                StructField(
                    "profile",
                    ReferenceSchema.get_schema(
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
