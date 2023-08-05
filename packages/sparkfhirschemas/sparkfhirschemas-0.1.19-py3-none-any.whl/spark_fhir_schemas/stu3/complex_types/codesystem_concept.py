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
class CodeSystem_ConceptSchema:
    """
    A code system resource specifies a set of codes drawn from one or more code
    systems.
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
        A code system resource specifies a set of codes drawn from one or more code
        systems.


        code: A code - a text symbol - that uniquely identifies the concept within the code
            system.

        display: A human readable string that is the recommended default way to present this
            concept to a user.

        definition: The formal definition of the concept. The code system resource does not make
            formal definitions required, because of the prevalence of legacy systems.
            However, they are highly recommended, as without them there is no formal
            meaning associated with the concept.

        designation: Additional representations for the concept - other languages, aliases,
            specialized purposes, used for particular purposes, etc.

        property: A property value for this concept.

        concept: Defines children of a concept to produce a hierarchy of concepts. The nature
            of the relationships is variable (is-a/contains/categorizes) - see
            hierarchyMeaning.

        """
        from spark_fhir_schemas.stu3.complex_types.codesystem_designation import CodeSystem_DesignationSchema
        from spark_fhir_schemas.stu3.complex_types.codesystem_property1 import CodeSystem_Property1Schema
        if (
            max_recursion_limit
            and nesting_list.count("CodeSystem_Concept") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["CodeSystem_Concept"]
        schema = StructType(
            [
                # A code - a text symbol - that uniquely identifies the concept within the code
                # system.
                StructField("code", StringType(), True),
                # A human readable string that is the recommended default way to present this
                # concept to a user.
                StructField("display", StringType(), True),
                # The formal definition of the concept. The code system resource does not make
                # formal definitions required, because of the prevalence of legacy systems.
                # However, they are highly recommended, as without them there is no formal
                # meaning associated with the concept.
                StructField("definition", StringType(), True),
                # Additional representations for the concept - other languages, aliases,
                # specialized purposes, used for particular purposes, etc.
                StructField(
                    "designation",
                    ArrayType(
                        CodeSystem_DesignationSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # A property value for this concept.
                StructField(
                    "property",
                    ArrayType(
                        CodeSystem_Property1Schema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Defines children of a concept to produce a hierarchy of concepts. The nature
                # of the relationships is variable (is-a/contains/categorizes) - see
                # hierarchyMeaning.
                StructField(
                    "concept",
                    ArrayType(
                        CodeSystem_ConceptSchema.get_schema(
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
