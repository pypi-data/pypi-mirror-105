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
class ImplementationGuide_PageSchema:
    """
    A set of rules of how FHIR is used to solve a particular problem. This
    resource is used to gather all the parts of an implementation guide into a
    logical whole and to publish a computable definition of all the parts.
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
        A set of rules of how FHIR is used to solve a particular problem. This
        resource is used to gather all the parts of an implementation guide into a
        logical whole and to publish a computable definition of all the parts.


        source: The source address for the page.

        title: A short title used to represent this page in navigational structures such as
            table of contents, bread crumbs, etc.

        kind: The kind of page that this is. Some pages are autogenerated (list, example),
            and other kinds are of interest so that tools can navigate the user to the
            page of interest.

        type: For constructed pages, what kind of resources to include in the list.

        package: For constructed pages, a list of packages to include in the page (or else
            empty for everything).

        format: The format of the page.

        page: Nested Pages/Sections under this page.

        """
        if (
            max_recursion_limit
            and nesting_list.count("ImplementationGuide_Page") >=
            max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + [
            "ImplementationGuide_Page"
        ]
        schema = StructType(
            [
                # The source address for the page.
                StructField("source", StringType(), True),
                # A short title used to represent this page in navigational structures such as
                # table of contents, bread crumbs, etc.
                StructField("title", StringType(), True),
                # The kind of page that this is. Some pages are autogenerated (list, example),
                # and other kinds are of interest so that tools can navigate the user to the
                # page of interest.
                StructField("kind", StringType(), True),
                # For constructed pages, what kind of resources to include in the list.
                # For constructed pages, a list of packages to include in the page (or else
                # empty for everything).
                # The format of the page.
                StructField("format", StringType(), True),
                # Nested Pages/Sections under this page.
                StructField(
                    "page",
                    ArrayType(
                        ImplementationGuide_PageSchema.get_schema(
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
