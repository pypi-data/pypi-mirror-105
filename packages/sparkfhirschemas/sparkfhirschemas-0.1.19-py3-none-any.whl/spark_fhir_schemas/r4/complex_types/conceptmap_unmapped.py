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
class ConceptMap_UnmappedSchema:
    """
    A statement of relationships from one set of concepts to one or more other
    concepts - either concepts in code systems, or data element/data element
    concepts, or classes in class models.
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
        A statement of relationships from one set of concepts to one or more other
        concepts - either concepts in code systems, or data element/data element
        concepts, or classes in class models.


        id: Unique id for the element within a resource (for internal references). This
            may be any string value that does not contain spaces.

        extension: May be used to represent additional information that is not part of the basic
            definition of the element. To make the use of extensions safe and manageable,
            there is a strict set of governance  applied to the definition and use of
            extensions. Though any implementer can define an extension, there is a set of
            requirements that SHALL be met as part of the definition of the extension.

        mode: Defines which action to take if there is no match for the source concept in
            the target system designated for the group. One of 3 actions are possible: use
            the unmapped code (this is useful when doing a mapping between versions, and
            only a few codes have changed), use a fixed code (a default code), or
            alternatively, a reference to a different concept map can be provided (by
            canonical URL).

        code: The fixed code to use when the mode = 'fixed'  - all unmapped codes are mapped
            to a single fixed code.

        display: The display for the code. The display is only provided to help editors when
            editing the concept map.

        url: The canonical reference to an additional ConceptMap resource instance to use
            for mapping if this ConceptMap resource contains no matching mapping for the
            source concept.

        """
        from spark_fhir_schemas.r4.complex_types.extension import ExtensionSchema
        from spark_fhir_schemas.r4.simple_types.code import codeSchema
        from spark_fhir_schemas.r4.simple_types.canonical import canonicalSchema
        if (
            max_recursion_limit and
            nesting_list.count("ConceptMap_Unmapped") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["ConceptMap_Unmapped"]
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
                # Defines which action to take if there is no match for the source concept in
                # the target system designated for the group. One of 3 actions are possible: use
                # the unmapped code (this is useful when doing a mapping between versions, and
                # only a few codes have changed), use a fixed code (a default code), or
                # alternatively, a reference to a different concept map can be provided (by
                # canonical URL).
                StructField("mode", StringType(), True),
                # The fixed code to use when the mode = 'fixed'  - all unmapped codes are mapped
                # to a single fixed code.
                StructField(
                    "code",
                    codeSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The display for the code. The display is only provided to help editors when
                # editing the concept map.
                StructField("display", StringType(), True),
                # The canonical reference to an additional ConceptMap resource instance to use
                # for mapping if this ConceptMap resource contains no matching mapping for the
                # source concept.
                StructField(
                    "url",
                    canonicalSchema.get_schema(
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
