from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import BooleanType
from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class ConceptMapSchema:
    """
    A statement of relationships from one set of concepts to one or more other
    concepts - either code systems or data elements, or classes in class models.
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
        concepts - either code systems or data elements, or classes in class models.


        resourceType: This is a ConceptMap resource

        url: An absolute URI that is used to identify this concept map when it is
            referenced in a specification, model, design or an instance. This SHALL be a
            URL, SHOULD be globally unique, and SHOULD be an address at which this concept
            map is (or will be) published. The URL SHOULD include the major version of the
            concept map. For more information see [Technical and Business
            Versions](resource.html#versions).

        identifier: A formal identifier that is used to identify this concept map when it is
            represented in other formats, or referenced in a specification, model, design
            or an instance.

        version: The identifier that is used to identify this version of the concept map when
            it is referenced in a specification, model, design or instance. This is an
            arbitrary value managed by the concept map author and is not expected to be
            globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a
            managed version is not available. There is also no expectation that versions
            can be placed in a lexicographical sequence.

        name: A natural language name identifying the concept map. This name should be
            usable as an identifier for the module by machine processing applications such
            as code generation.

        title: A short, descriptive, user-friendly title for the concept map.

        status: The status of this concept map. Enables tracking the life-cycle of the
            content.

        experimental: A boolean value to indicate that this concept map is authored for testing
            purposes (or education/evaluation/marketing), and is not intended to be used
            for genuine usage.

        date: The date  (and optionally time) when the concept map was published. The date
            must change if and when the business version changes and it must change if the
            status code changes. In addition, it should change when the substantive
            content of the concept map changes.

        publisher: The name of the individual or organization that published the concept map.

        contact: Contact details to assist a user in finding and communicating with the
            publisher.

        description: A free text natural language description of the concept map from a consumer's
            perspective.

        useContext: The content was developed with a focus and intent of supporting the contexts
            that are listed. These terms may be used to assist with indexing and searching
            for appropriate concept map instances.

        jurisdiction: A legal or geographic region in which the concept map is intended to be used.

        purpose: Explaination of why this concept map is needed and why it has been designed as
            it has.

        copyright: A copyright statement relating to the concept map and/or its contents.
            Copyright statements are generally legal restrictions on the use and
            publishing of the concept map.

        sourceUri: The source value set that specifies the concepts that are being mapped.

        sourceReference: The source value set that specifies the concepts that are being mapped.

        targetUri: The target value set provides context to the mappings. Note that the mapping
            is made between concepts, not between value sets, but the value set provides
            important context about how the concept mapping choices are made.

        targetReference: The target value set provides context to the mappings. Note that the mapping
            is made between concepts, not between value sets, but the value set provides
            important context about how the concept mapping choices are made.

        group: A group of mappings that all have the same source and target system.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.contactdetail import ContactDetailSchema
        from spark_fhir_schemas.stu3.complex_types.usagecontext import UsageContextSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.conceptmap_group import ConceptMap_GroupSchema
        if (
            max_recursion_limit
            and nesting_list.count("ConceptMap") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["ConceptMap"]
        schema = StructType(
            [
                # This is a ConceptMap resource
                StructField("resourceType", StringType(), True),
                # An absolute URI that is used to identify this concept map when it is
                # referenced in a specification, model, design or an instance. This SHALL be a
                # URL, SHOULD be globally unique, and SHOULD be an address at which this concept
                # map is (or will be) published. The URL SHOULD include the major version of the
                # concept map. For more information see [Technical and Business
                # Versions](resource.html#versions).
                StructField("url", StringType(), True),
                # A formal identifier that is used to identify this concept map when it is
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
                # The identifier that is used to identify this version of the concept map when
                # it is referenced in a specification, model, design or instance. This is an
                # arbitrary value managed by the concept map author and is not expected to be
                # globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a
                # managed version is not available. There is also no expectation that versions
                # can be placed in a lexicographical sequence.
                StructField("version", StringType(), True),
                # A natural language name identifying the concept map. This name should be
                # usable as an identifier for the module by machine processing applications such
                # as code generation.
                StructField("name", StringType(), True),
                # A short, descriptive, user-friendly title for the concept map.
                StructField("title", StringType(), True),
                # The status of this concept map. Enables tracking the life-cycle of the
                # content.
                StructField("status", StringType(), True),
                # A boolean value to indicate that this concept map is authored for testing
                # purposes (or education/evaluation/marketing), and is not intended to be used
                # for genuine usage.
                StructField("experimental", BooleanType(), True),
                # The date  (and optionally time) when the concept map was published. The date
                # must change if and when the business version changes and it must change if the
                # status code changes. In addition, it should change when the substantive
                # content of the concept map changes.
                StructField("date", StringType(), True),
                # The name of the individual or organization that published the concept map.
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
                # A free text natural language description of the concept map from a consumer's
                # perspective.
                StructField("description", StringType(), True),
                # The content was developed with a focus and intent of supporting the contexts
                # that are listed. These terms may be used to assist with indexing and searching
                # for appropriate concept map instances.
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
                # A legal or geographic region in which the concept map is intended to be used.
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
                # Explaination of why this concept map is needed and why it has been designed as
                # it has.
                StructField("purpose", StringType(), True),
                # A copyright statement relating to the concept map and/or its contents.
                # Copyright statements are generally legal restrictions on the use and
                # publishing of the concept map.
                StructField("copyright", StringType(), True),
                # The source value set that specifies the concepts that are being mapped.
                StructField("sourceUri", StringType(), True),
                # The source value set that specifies the concepts that are being mapped.
                StructField(
                    "sourceReference",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The target value set provides context to the mappings. Note that the mapping
                # is made between concepts, not between value sets, but the value set provides
                # important context about how the concept mapping choices are made.
                StructField("targetUri", StringType(), True),
                # The target value set provides context to the mappings. Note that the mapping
                # is made between concepts, not between value sets, but the value set provides
                # important context about how the concept mapping choices are made.
                StructField(
                    "targetReference",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A group of mappings that all have the same source and target system.
                StructField(
                    "group",
                    ArrayType(
                        ConceptMap_GroupSchema.get_schema(
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
