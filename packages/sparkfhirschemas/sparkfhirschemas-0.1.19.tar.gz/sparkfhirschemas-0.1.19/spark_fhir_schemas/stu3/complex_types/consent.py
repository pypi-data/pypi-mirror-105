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
class ConsentSchema:
    """
    A record of a healthcare consumer’s policy choices, which permits or denies
    identified recipient(s) or recipient role(s) to perform one or more actions
    within a given policy context, for specific purposes and periods of time.
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
        A record of a healthcare consumer’s policy choices, which permits or denies
        identified recipient(s) or recipient role(s) to perform one or more actions
        within a given policy context, for specific purposes and periods of time.


        resourceType: This is a Consent resource

        identifier: Unique identifier for this copy of the Consent Statement.

        status: Indicates the current state of this consent.

        category: A classification of the type of consents found in the statement. This element
            supports indexing and retrieval of consent statements.

        patient: The patient/healthcare consumer to whom this consent applies.

        period: Relevant time or time-period when this Consent is applicable.

        dateTime: When this  Consent was issued / created / indexed.

        consentingParty: Either the Grantor, which is the entity responsible for granting the rights
            listed in a Consent Directive or the Grantee, which is the entity responsible
            for complying with the Consent Directive, including any obligations or
            limitations on authorizations and enforcement of prohibitions.

        actor: Who or what is controlled by this consent. Use group to identify a set of
            actors by some property they share (e.g. 'admitting officers').

        action: Actions controlled by this consent.

        organization: The organization that manages the consent, and the framework within which it
            is executed.

        sourceAttachment: The source on which this consent statement is based. The source might be a
            scanned original paper form, or a reference to a consent that links back to
            such a source, a reference to a document repository (e.g. XDS) that stores the
            original consent document.

        sourceIdentifier: The source on which this consent statement is based. The source might be a
            scanned original paper form, or a reference to a consent that links back to
            such a source, a reference to a document repository (e.g. XDS) that stores the
            original consent document.

        sourceReference: The source on which this consent statement is based. The source might be a
            scanned original paper form, or a reference to a consent that links back to
            such a source, a reference to a document repository (e.g. XDS) that stores the
            original consent document.

        policy: The references to the policies that are included in this consent scope.
            Policies may be organizational, but are often defined jurisdictionally, or in
            law.

        policyRule: A referece to the specific computable policy.

        securityLabel: A set of security labels that define which resources are controlled by this
            consent. If more than one label is specified, all resources must have all the
            specified labels.

        purpose: The context of the activities a user is taking - why the user is accessing the
            data - that are controlled by this consent.

        dataPeriod: Clinical or Operational Relevant period of time that bounds the data
            controlled by this consent.

        data: The resources controlled by this consent, if specific resources are
            referenced.

        except: An exception to the base policy of this consent. An exception can be an
            addition or removal of access permissions.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.period import PeriodSchema
        from spark_fhir_schemas.stu3.complex_types.consent_actor import Consent_ActorSchema
        from spark_fhir_schemas.stu3.complex_types.attachment import AttachmentSchema
        from spark_fhir_schemas.stu3.complex_types.consent_policy import Consent_PolicySchema
        from spark_fhir_schemas.stu3.complex_types.coding import CodingSchema
        from spark_fhir_schemas.stu3.complex_types.consent_data import Consent_DataSchema
        from spark_fhir_schemas.stu3.complex_types.consent_except import Consent_ExceptSchema
        if (
            max_recursion_limit
            and nesting_list.count("Consent") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Consent"]
        schema = StructType(
            [
                # This is a Consent resource
                StructField("resourceType", StringType(), True),
                # Unique identifier for this copy of the Consent Statement.
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
                # Indicates the current state of this consent.
                StructField("status", StringType(), True),
                # A classification of the type of consents found in the statement. This element
                # supports indexing and retrieval of consent statements.
                StructField(
                    "category",
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
                # The patient/healthcare consumer to whom this consent applies.
                StructField(
                    "patient",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Relevant time or time-period when this Consent is applicable.
                StructField(
                    "period",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # When this  Consent was issued / created / indexed.
                StructField("dateTime", StringType(), True),
                # Either the Grantor, which is the entity responsible for granting the rights
                # listed in a Consent Directive or the Grantee, which is the entity responsible
                # for complying with the Consent Directive, including any obligations or
                # limitations on authorizations and enforcement of prohibitions.
                StructField(
                    "consentingParty",
                    ArrayType(
                        ReferenceSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Who or what is controlled by this consent. Use group to identify a set of
                # actors by some property they share (e.g. 'admitting officers').
                StructField(
                    "actor",
                    ArrayType(
                        Consent_ActorSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Actions controlled by this consent.
                StructField(
                    "action",
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
                # The organization that manages the consent, and the framework within which it
                # is executed.
                StructField(
                    "organization",
                    ArrayType(
                        ReferenceSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # The source on which this consent statement is based. The source might be a
                # scanned original paper form, or a reference to a consent that links back to
                # such a source, a reference to a document repository (e.g. XDS) that stores the
                # original consent document.
                StructField(
                    "sourceAttachment",
                    AttachmentSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The source on which this consent statement is based. The source might be a
                # scanned original paper form, or a reference to a consent that links back to
                # such a source, a reference to a document repository (e.g. XDS) that stores the
                # original consent document.
                StructField(
                    "sourceIdentifier",
                    IdentifierSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The source on which this consent statement is based. The source might be a
                # scanned original paper form, or a reference to a consent that links back to
                # such a source, a reference to a document repository (e.g. XDS) that stores the
                # original consent document.
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
                # The references to the policies that are included in this consent scope.
                # Policies may be organizational, but are often defined jurisdictionally, or in
                # law.
                StructField(
                    "policy",
                    ArrayType(
                        Consent_PolicySchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # A referece to the specific computable policy.
                StructField("policyRule", StringType(), True),
                # A set of security labels that define which resources are controlled by this
                # consent. If more than one label is specified, all resources must have all the
                # specified labels.
                StructField(
                    "securityLabel",
                    ArrayType(
                        CodingSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # The context of the activities a user is taking - why the user is accessing the
                # data - that are controlled by this consent.
                StructField(
                    "purpose",
                    ArrayType(
                        CodingSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Clinical or Operational Relevant period of time that bounds the data
                # controlled by this consent.
                StructField(
                    "dataPeriod",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The resources controlled by this consent, if specific resources are
                # referenced.
                StructField(
                    "data",
                    ArrayType(
                        Consent_DataSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # An exception to the base policy of this consent. An exception can be an
                # addition or removal of access permissions.
                StructField(
                    "except",
                    ArrayType(
                        Consent_ExceptSchema.get_schema(
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
