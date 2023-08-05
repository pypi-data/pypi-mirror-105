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
class AuditEvent_AgentSchema:
    """
    A record of an event made for purposes of maintaining a security log. Typical
    uses include detection of intrusion attempts and monitoring for inappropriate
    usage.
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
        A record of an event made for purposes of maintaining a security log. Typical
        uses include detection of intrusion attempts and monitoring for inappropriate
        usage.


        role: The security role that the user was acting under, that come from local codes
            defined by the access control security system (e.g. RBAC, ABAC) used in the
            local context.

        reference: Direct reference to a resource that identifies the agent.

        userId: Unique identifier for the user actively participating in the event.

        altId: Alternative agent Identifier. For a human, this should be a user identifier
            text string from authentication system. This identifier would be one known to
            a common authentication system (e.g. single sign-on), if available.

        name: Human-meaningful name for the agent.

        requestor: Indicator that the user is or is not the requestor, or initiator, for the
            event being audited.

        location: Where the event occurred.

        policy: The policy or plan that authorized the activity being recorded. Typically, a
            single activity may have multiple applicable policies, such as patient
            consent, guarantor funding, etc. The policy would also indicate the security
            token used.

        media: Type of media involved. Used when the event is about exporting/importing onto
            media.

        network: Logical network location for application activity, if the activity has a
            network location.

        purposeOfUse: The reason (purpose of use), specific to this agent, that was used during the
            event being recorded.

        """
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.coding import CodingSchema
        from spark_fhir_schemas.stu3.complex_types.auditevent_network import AuditEvent_NetworkSchema
        if (
            max_recursion_limit
            and nesting_list.count("AuditEvent_Agent") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["AuditEvent_Agent"]
        schema = StructType(
            [
                # The security role that the user was acting under, that come from local codes
                # defined by the access control security system (e.g. RBAC, ABAC) used in the
                # local context.
                StructField(
                    "role",
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
                # Direct reference to a resource that identifies the agent.
                StructField(
                    "reference",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Unique identifier for the user actively participating in the event.
                StructField(
                    "userId",
                    IdentifierSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Alternative agent Identifier. For a human, this should be a user identifier
                # text string from authentication system. This identifier would be one known to
                # a common authentication system (e.g. single sign-on), if available.
                StructField("altId", StringType(), True),
                # Human-meaningful name for the agent.
                StructField("name", StringType(), True),
                # Indicator that the user is or is not the requestor, or initiator, for the
                # event being audited.
                StructField("requestor", BooleanType(), True),
                # Where the event occurred.
                StructField(
                    "location",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The policy or plan that authorized the activity being recorded. Typically, a
                # single activity may have multiple applicable policies, such as patient
                # consent, guarantor funding, etc. The policy would also indicate the security
                # token used.
                # Type of media involved. Used when the event is about exporting/importing onto
                # media.
                StructField(
                    "media",
                    CodingSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Logical network location for application activity, if the activity has a
                # network location.
                StructField(
                    "network",
                    AuditEvent_NetworkSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The reason (purpose of use), specific to this agent, that was used during the
                # event being recorded.
                StructField(
                    "purposeOfUse",
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
            ]
        )
        if not include_extension:
            schema.fields = [
                c if c.name != "extension" else
                StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
