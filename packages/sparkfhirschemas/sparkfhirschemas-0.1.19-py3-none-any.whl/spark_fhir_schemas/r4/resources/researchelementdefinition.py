from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import BooleanType
from pyspark.sql.types import DataType
from pyspark.sql.types import DateType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class ResearchElementDefinitionSchema:
    """
    The ResearchElementDefinition resource describes a "PICO" element that
    knowledge (evidence, assertion, recommendation) is about.
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
        The ResearchElementDefinition resource describes a "PICO" element that
        knowledge (evidence, assertion, recommendation) is about.


        resourceType: This is a ResearchElementDefinition resource

        id: The logical id of the resource, as used in the URL for the resource. Once
            assigned, this value never changes.

        meta: The metadata about the resource. This is content that is maintained by the
            infrastructure. Changes to the content might not always be associated with
            version changes to the resource.

        implicitRules: A reference to a set of rules that were followed when the resource was
            constructed, and which must be understood when processing the content. Often,
            this is a reference to an implementation guide that defines the special rules
            along with other profiles etc.

        language: The base language in which the resource is written.

        text: A human-readable narrative that contains a summary of the resource and can be
            used to represent the content of the resource to a human. The narrative need
            not encode all the structured data, but is required to contain sufficient
            detail to make it "clinically safe" for a human to just read the narrative.
            Resource definitions may define what content should be represented in the
            narrative to ensure clinical safety.

        contained: These resources do not have an independent existence apart from the resource
            that contains them - they cannot be identified independently, and nor can they
            have their own independent transaction scope.

        extension: May be used to represent additional information that is not part of the basic
            definition of the resource. To make the use of extensions safe and manageable,
            there is a strict set of governance  applied to the definition and use of
            extensions. Though any implementer can define an extension, there is a set of
            requirements that SHALL be met as part of the definition of the extension.

        url: An absolute URI that is used to identify this research element definition when
            it is referenced in a specification, model, design or an instance; also called
            its canonical identifier. This SHOULD be globally unique and SHOULD be a
            literal address at which at which an authoritative instance of this research
            element definition is (or will be) published. This URL can be the target of a
            canonical reference. It SHALL remain the same when the research element
            definition is stored on different servers.

        identifier: A formal identifier that is used to identify this research element definition
            when it is represented in other formats, or referenced in a specification,
            model, design or an instance.

        version: The identifier that is used to identify this version of the research element
            definition when it is referenced in a specification, model, design or
            instance. This is an arbitrary value managed by the research element
            definition author and is not expected to be globally unique. For example, it
            might be a timestamp (e.g. yyyymmdd) if a managed version is not available.
            There is also no expectation that versions can be placed in a lexicographical
            sequence. To provide a version consistent with the Decision Support Service
            specification, use the format Major.Minor.Revision (e.g. 1.0.0). For more
            information on versioning knowledge assets, refer to the Decision Support
            Service specification. Note that a version is required for non-experimental
            active artifacts.

        name: A natural language name identifying the research element definition. This name
            should be usable as an identifier for the module by machine processing
            applications such as code generation.

        title: A short, descriptive, user-friendly title for the research element definition.

        shortTitle: The short title provides an alternate title for use in informal descriptive
            contexts where the full, formal title is not necessary.

        subtitle: An explanatory or alternate title for the ResearchElementDefinition giving
            additional information about its content.

        status: The status of this research element definition. Enables tracking the life-
            cycle of the content.

        experimental: A Boolean value to indicate that this research element definition is authored
            for testing purposes (or education/evaluation/marketing) and is not intended
            to be used for genuine usage.

        subjectCodeableConcept: The intended subjects for the ResearchElementDefinition. If this element is
            not provided, a Patient subject is assumed, but the subject of the
            ResearchElementDefinition can be anything.

        subjectReference: The intended subjects for the ResearchElementDefinition. If this element is
            not provided, a Patient subject is assumed, but the subject of the
            ResearchElementDefinition can be anything.

        date: The date  (and optionally time) when the research element definition was
            published. The date must change when the business version changes and it must
            change if the status code changes. In addition, it should change when the
            substantive content of the research element definition changes.

        publisher: The name of the organization or individual that published the research element
            definition.

        contact: Contact details to assist a user in finding and communicating with the
            publisher.

        description: A free text natural language description of the research element definition
            from a consumer's perspective.

        comment: A human-readable string to clarify or explain concepts about the resource.

        useContext: The content was developed with a focus and intent of supporting the contexts
            that are listed. These contexts may be general categories (gender, age, ...)
            or may be references to specific programs (insurance plans, studies, ...) and
            may be used to assist with indexing and searching for appropriate research
            element definition instances.

        jurisdiction: A legal or geographic region in which the research element definition is
            intended to be used.

        purpose: Explanation of why this research element definition is needed and why it has
            been designed as it has.

        usage: A detailed description, from a clinical perspective, of how the
            ResearchElementDefinition is used.

        copyright: A copyright statement relating to the research element definition and/or its
            contents. Copyright statements are generally legal restrictions on the use and
            publishing of the research element definition.

        approvalDate: The date on which the resource content was approved by the publisher. Approval
            happens once when the content is officially approved for usage.

        lastReviewDate: The date on which the resource content was last reviewed. Review happens
            periodically after approval but does not change the original approval date.

        effectivePeriod: The period during which the research element definition content was or is
            planned to be in active use.

        topic: Descriptive topics related to the content of the ResearchElementDefinition.
            Topics provide a high-level categorization grouping types of
            ResearchElementDefinitions that can be useful for filtering and searching.

        author: An individiual or organization primarily involved in the creation and
            maintenance of the content.

        editor: An individual or organization primarily responsible for internal coherence of
            the content.

        reviewer: An individual or organization primarily responsible for review of some aspect
            of the content.

        endorser: An individual or organization responsible for officially endorsing the content
            for use in some setting.

        relatedArtifact: Related artifacts such as additional documentation, justification, or
            bibliographic references.

        library: A reference to a Library resource containing the formal logic used by the
            ResearchElementDefinition.

        type: The type of research element, a population, an exposure, or an outcome.

        variableType: The type of the outcome (e.g. Dichotomous, Continuous, or Descriptive).

        characteristic: A characteristic that defines the members of the research element. Multiple
            characteristics are applied with "and" semantics.

        """
        from spark_fhir_schemas.r4.simple_types.id import idSchema
        from spark_fhir_schemas.r4.complex_types.meta import MetaSchema
        from spark_fhir_schemas.r4.simple_types.uri import uriSchema
        from spark_fhir_schemas.r4.simple_types.code import codeSchema
        from spark_fhir_schemas.r4.complex_types.narrative import NarrativeSchema
        from spark_fhir_schemas.r4.complex_types.resourcelist import ResourceListSchema
        from spark_fhir_schemas.r4.complex_types.extension import ExtensionSchema
        from spark_fhir_schemas.r4.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.r4.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.r4.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.r4.simple_types.datetime import dateTimeSchema
        from spark_fhir_schemas.r4.complex_types.contactdetail import ContactDetailSchema
        from spark_fhir_schemas.r4.simple_types.markdown import markdownSchema
        from spark_fhir_schemas.r4.complex_types.usagecontext import UsageContextSchema
        from spark_fhir_schemas.r4.complex_types.period import PeriodSchema
        from spark_fhir_schemas.r4.complex_types.relatedartifact import RelatedArtifactSchema
        from spark_fhir_schemas.r4.simple_types.canonical import canonicalSchema
        from spark_fhir_schemas.r4.complex_types.researchelementdefinition_characteristic import ResearchElementDefinition_CharacteristicSchema
        if (
            max_recursion_limit
            and nesting_list.count("ResearchElementDefinition") >=
            max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + [
            "ResearchElementDefinition"
        ]
        schema = StructType(
            [
                # This is a ResearchElementDefinition resource
                StructField("resourceType", StringType(), True),
                # The logical id of the resource, as used in the URL for the resource. Once
                # assigned, this value never changes.
                StructField(
                    "id",
                    idSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The metadata about the resource. This is content that is maintained by the
                # infrastructure. Changes to the content might not always be associated with
                # version changes to the resource.
                StructField(
                    "meta",
                    MetaSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A reference to a set of rules that were followed when the resource was
                # constructed, and which must be understood when processing the content. Often,
                # this is a reference to an implementation guide that defines the special rules
                # along with other profiles etc.
                StructField(
                    "implicitRules",
                    uriSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The base language in which the resource is written.
                StructField(
                    "language",
                    codeSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A human-readable narrative that contains a summary of the resource and can be
                # used to represent the content of the resource to a human. The narrative need
                # not encode all the structured data, but is required to contain sufficient
                # detail to make it "clinically safe" for a human to just read the narrative.
                # Resource definitions may define what content should be represented in the
                # narrative to ensure clinical safety.
                StructField(
                    "text",
                    NarrativeSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # These resources do not have an independent existence apart from the resource
                # that contains them - they cannot be identified independently, and nor can they
                # have their own independent transaction scope.
                StructField(
                    "contained",
                    ArrayType(
                        ResourceListSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # May be used to represent additional information that is not part of the basic
                # definition of the resource. To make the use of extensions safe and manageable,
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
                # An absolute URI that is used to identify this research element definition when
                # it is referenced in a specification, model, design or an instance; also called
                # its canonical identifier. This SHOULD be globally unique and SHOULD be a
                # literal address at which at which an authoritative instance of this research
                # element definition is (or will be) published. This URL can be the target of a
                # canonical reference. It SHALL remain the same when the research element
                # definition is stored on different servers.
                StructField(
                    "url",
                    uriSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A formal identifier that is used to identify this research element definition
                # when it is represented in other formats, or referenced in a specification,
                # model, design or an instance.
                StructField(
                    "identifier",
                    ArrayType(
                        IdentifierSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # The identifier that is used to identify this version of the research element
                # definition when it is referenced in a specification, model, design or
                # instance. This is an arbitrary value managed by the research element
                # definition author and is not expected to be globally unique. For example, it
                # might be a timestamp (e.g. yyyymmdd) if a managed version is not available.
                # There is also no expectation that versions can be placed in a lexicographical
                # sequence. To provide a version consistent with the Decision Support Service
                # specification, use the format Major.Minor.Revision (e.g. 1.0.0). For more
                # information on versioning knowledge assets, refer to the Decision Support
                # Service specification. Note that a version is required for non-experimental
                # active artifacts.
                StructField("version", StringType(), True),
                # A natural language name identifying the research element definition. This name
                # should be usable as an identifier for the module by machine processing
                # applications such as code generation.
                StructField("name", StringType(), True),
                # A short, descriptive, user-friendly title for the research element definition.
                StructField("title", StringType(), True),
                # The short title provides an alternate title for use in informal descriptive
                # contexts where the full, formal title is not necessary.
                StructField("shortTitle", StringType(), True),
                # An explanatory or alternate title for the ResearchElementDefinition giving
                # additional information about its content.
                StructField("subtitle", StringType(), True),
                # The status of this research element definition. Enables tracking the life-
                # cycle of the content.
                StructField("status", StringType(), True),
                # A Boolean value to indicate that this research element definition is authored
                # for testing purposes (or education/evaluation/marketing) and is not intended
                # to be used for genuine usage.
                StructField("experimental", BooleanType(), True),
                # The intended subjects for the ResearchElementDefinition. If this element is
                # not provided, a Patient subject is assumed, but the subject of the
                # ResearchElementDefinition can be anything.
                StructField(
                    "subjectCodeableConcept",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The intended subjects for the ResearchElementDefinition. If this element is
                # not provided, a Patient subject is assumed, but the subject of the
                # ResearchElementDefinition can be anything.
                StructField(
                    "subjectReference",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The date  (and optionally time) when the research element definition was
                # published. The date must change when the business version changes and it must
                # change if the status code changes. In addition, it should change when the
                # substantive content of the research element definition changes.
                StructField(
                    "date",
                    dateTimeSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The name of the organization or individual that published the research element
                # definition.
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
                # A free text natural language description of the research element definition
                # from a consumer's perspective.
                StructField(
                    "description",
                    markdownSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A human-readable string to clarify or explain concepts about the resource.
                StructField("comment", ArrayType(StringType()), True),
                # The content was developed with a focus and intent of supporting the contexts
                # that are listed. These contexts may be general categories (gender, age, ...)
                # or may be references to specific programs (insurance plans, studies, ...) and
                # may be used to assist with indexing and searching for appropriate research
                # element definition instances.
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
                # A legal or geographic region in which the research element definition is
                # intended to be used.
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
                # Explanation of why this research element definition is needed and why it has
                # been designed as it has.
                StructField(
                    "purpose",
                    markdownSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A detailed description, from a clinical perspective, of how the
                # ResearchElementDefinition is used.
                StructField("usage", StringType(), True),
                # A copyright statement relating to the research element definition and/or its
                # contents. Copyright statements are generally legal restrictions on the use and
                # publishing of the research element definition.
                StructField(
                    "copyright",
                    markdownSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The date on which the resource content was approved by the publisher. Approval
                # happens once when the content is officially approved for usage.
                StructField("approvalDate", DateType(), True),
                # The date on which the resource content was last reviewed. Review happens
                # periodically after approval but does not change the original approval date.
                StructField("lastReviewDate", DateType(), True),
                # The period during which the research element definition content was or is
                # planned to be in active use.
                StructField(
                    "effectivePeriod",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Descriptive topics related to the content of the ResearchElementDefinition.
                # Topics provide a high-level categorization grouping types of
                # ResearchElementDefinitions that can be useful for filtering and searching.
                StructField(
                    "topic",
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
                # An individiual or organization primarily involved in the creation and
                # maintenance of the content.
                StructField(
                    "author",
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
                # An individual or organization primarily responsible for internal coherence of
                # the content.
                StructField(
                    "editor",
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
                # An individual or organization primarily responsible for review of some aspect
                # of the content.
                StructField(
                    "reviewer",
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
                # An individual or organization responsible for officially endorsing the content
                # for use in some setting.
                StructField(
                    "endorser",
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
                # Related artifacts such as additional documentation, justification, or
                # bibliographic references.
                StructField(
                    "relatedArtifact",
                    ArrayType(
                        RelatedArtifactSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # A reference to a Library resource containing the formal logic used by the
                # ResearchElementDefinition.
                StructField(
                    "library",
                    ArrayType(
                        canonicalSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # The type of research element, a population, an exposure, or an outcome.
                StructField("type", StringType(), True),
                # The type of the outcome (e.g. Dichotomous, Continuous, or Descriptive).
                StructField("variableType", StringType(), True),
                # A characteristic that defines the members of the research element. Multiple
                # characteristics are applied with "and" semantics.
                StructField(
                    "characteristic",
                    ArrayType(
                        ResearchElementDefinition_CharacteristicSchema.
                        get_schema(
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
