from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import BooleanType
from pyspark.sql.types import DataType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class CodeSystemSchema:
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


        resourceType: This is a CodeSystem resource

        url: An absolute URI that is used to identify this code system when it is
            referenced in a specification, model, design or an instance. This SHALL be a
            URL, SHOULD be globally unique, and SHOULD be an address at which this code
            system is (or will be) published. The URL SHOULD include the major version of
            the code system. For more information see [Technical and Business
            Versions](resource.html#versions). This is used in
            [Coding]{datatypes.html#Coding}.system.

        identifier: A formal identifier that is used to identify this code system when it is
            represented in other formats, or referenced in a specification, model, design
            or an instance.

        version: The identifier that is used to identify this version of the code system when
            it is referenced in a specification, model, design or instance. This is an
            arbitrary value managed by the code system author and is not expected to be
            globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a
            managed version is not available. There is also no expectation that versions
            can be placed in a lexicographical sequence. This is used in
            [Coding]{datatypes.html#Coding}.version.

        name: A natural language name identifying the code system. This name should be
            usable as an identifier for the module by machine processing applications such
            as code generation.

        title: A short, descriptive, user-friendly title for the code system.

        status: The status of this code system. Enables tracking the life-cycle of the
            content.

        experimental: A boolean value to indicate that this code system is authored for testing
            purposes (or education/evaluation/marketing), and is not intended to be used
            for genuine usage.

        date: The date  (and optionally time) when the code system was published. The date
            must change if and when the business version changes and it must change if the
            status code changes. In addition, it should change when the substantive
            content of the code system changes.

        publisher: The name of the individual or organization that published the code system.

        contact: Contact details to assist a user in finding and communicating with the
            publisher.

        description: A free text natural language description of the code system from a consumer's
            perspective.

        useContext: The content was developed with a focus and intent of supporting the contexts
            that are listed. These terms may be used to assist with indexing and searching
            for appropriate code system instances.

        jurisdiction: A legal or geographic region in which the code system is intended to be used.

        purpose: Explaination of why this code system is needed and why it has been designed as
            it has.

        copyright: A copyright statement relating to the code system and/or its contents.
            Copyright statements are generally legal restrictions on the use and
            publishing of the code system.

        caseSensitive: If code comparison is case sensitive when codes within this system are
            compared to each other.

        valueSet: Canonical URL of value set that contains the entire code system.

        hierarchyMeaning: The meaning of the hierarchy of concepts.

        compositional: True If code system defines a post-composition grammar.

        versionNeeded: This flag is used to signify that the code system has not (or does not)
            maintain the definitions, and a version must be specified when referencing
            this code system.

        content: How much of the content of the code system - the concepts and codes it defines
            - are represented in this resource.

        count: The total number of concepts defined by the code system. Where the code system
            has a compositional grammar, the count refers to the number of base
            (primitive) concepts.

        filter: A filter that can be used in a value set compose statement when selecting
            concepts using a filter.

        property: A property defines an additional slot through which additional information can
            be provided about a concept.

        concept: Concepts that are in the code system. The concept definitions are inherently
            hierarchical, but the definitions must be consulted to determine what the
            meaning of the hierarchical relationships are.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.contactdetail import ContactDetailSchema
        from spark_fhir_schemas.stu3.complex_types.usagecontext import UsageContextSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.stu3.complex_types.codesystem_filter import CodeSystem_FilterSchema
        from spark_fhir_schemas.stu3.complex_types.codesystem_property import CodeSystem_PropertySchema
        from spark_fhir_schemas.stu3.complex_types.codesystem_concept import CodeSystem_ConceptSchema
        if (
            max_recursion_limit
            and nesting_list.count("CodeSystem") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["CodeSystem"]
        schema = StructType(
            [
                # This is a CodeSystem resource
                StructField("resourceType", StringType(), True),
                # An absolute URI that is used to identify this code system when it is
                # referenced in a specification, model, design or an instance. This SHALL be a
                # URL, SHOULD be globally unique, and SHOULD be an address at which this code
                # system is (or will be) published. The URL SHOULD include the major version of
                # the code system. For more information see [Technical and Business
                # Versions](resource.html#versions). This is used in
                # [Coding]{datatypes.html#Coding}.system.
                StructField("url", StringType(), True),
                # A formal identifier that is used to identify this code system when it is
                # represented in other formats, or referenced in a specification, model, design
                # or an instance.
                StructField(
                    "identifier",
                    IdentifierSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The identifier that is used to identify this version of the code system when
                # it is referenced in a specification, model, design or instance. This is an
                # arbitrary value managed by the code system author and is not expected to be
                # globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a
                # managed version is not available. There is also no expectation that versions
                # can be placed in a lexicographical sequence. This is used in
                # [Coding]{datatypes.html#Coding}.version.
                StructField("version", StringType(), True),
                # A natural language name identifying the code system. This name should be
                # usable as an identifier for the module by machine processing applications such
                # as code generation.
                StructField("name", StringType(), True),
                # A short, descriptive, user-friendly title for the code system.
                StructField("title", StringType(), True),
                # The status of this code system. Enables tracking the life-cycle of the
                # content.
                StructField("status", StringType(), True),
                # A boolean value to indicate that this code system is authored for testing
                # purposes (or education/evaluation/marketing), and is not intended to be used
                # for genuine usage.
                StructField("experimental", BooleanType(), True),
                # The date  (and optionally time) when the code system was published. The date
                # must change if and when the business version changes and it must change if the
                # status code changes. In addition, it should change when the substantive
                # content of the code system changes.
                StructField("date", StringType(), True),
                # The name of the individual or organization that published the code system.
                StructField("publisher", StringType(), True),
                # Contact details to assist a user in finding and communicating with the
                # publisher.
                StructField(
                    "contact",
                    ArrayType(
                        ContactDetailSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # A free text natural language description of the code system from a consumer's
                # perspective.
                StructField("description", StringType(), True),
                # The content was developed with a focus and intent of supporting the contexts
                # that are listed. These terms may be used to assist with indexing and searching
                # for appropriate code system instances.
                StructField(
                    "useContext",
                    ArrayType(
                        UsageContextSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # A legal or geographic region in which the code system is intended to be used.
                StructField(
                    "jurisdiction",
                    ArrayType(
                        CodeableConceptSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Explaination of why this code system is needed and why it has been designed as
                # it has.
                StructField("purpose", StringType(), True),
                # A copyright statement relating to the code system and/or its contents.
                # Copyright statements are generally legal restrictions on the use and
                # publishing of the code system.
                StructField("copyright", StringType(), True),
                # If code comparison is case sensitive when codes within this system are
                # compared to each other.
                StructField("caseSensitive", BooleanType(), True),
                # Canonical URL of value set that contains the entire code system.
                StructField("valueSet", StringType(), True),
                # The meaning of the hierarchy of concepts.
                StructField("hierarchyMeaning", StringType(), True),
                # True If code system defines a post-composition grammar.
                StructField("compositional", BooleanType(), True),
                # This flag is used to signify that the code system has not (or does not)
                # maintain the definitions, and a version must be specified when referencing
                # this code system.
                StructField("versionNeeded", BooleanType(), True),
                # How much of the content of the code system - the concepts and codes it defines
                # - are represented in this resource.
                StructField("content", StringType(), True),
                # The total number of concepts defined by the code system. Where the code system
                # has a compositional grammar, the count refers to the number of base
                # (primitive) concepts.
                StructField("count", IntegerType(), True),
                # A filter that can be used in a value set compose statement when selecting
                # concepts using a filter.
                StructField(
                    "filter",
                    ArrayType(
                        CodeSystem_FilterSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # A property defines an additional slot through which additional information can
                # be provided about a concept.
                StructField(
                    "property",
                    ArrayType(
                        CodeSystem_PropertySchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Concepts that are in the code system. The concept definitions are inherently
                # hierarchical, but the definitions must be consulted to determine what the
                # meaning of the hierarchical relationships are.
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
