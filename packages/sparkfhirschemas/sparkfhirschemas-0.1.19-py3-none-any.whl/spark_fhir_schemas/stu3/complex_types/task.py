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
class TaskSchema:
    """
    A task to be performed.
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
        A task to be performed.


        resourceType: This is a Task resource

        identifier: The business identifier for this task.

        definitionUri: A reference to a formal or informal definition of the task.  For example, a
            protocol, a step within a defined workflow definition, etc.

        definitionReference: A reference to a formal or informal definition of the task.  For example, a
            protocol, a step within a defined workflow definition, etc.

        basedOn: BasedOn refers to a higher-level authorization that triggered the creation of
            the task.  It references a "request" resource such as a ProcedureRequest,
            MedicationRequest, ProcedureRequest, CarePlan, etc. which is distinct from the
            "request" resource the task is seeking to fulfil.  This latter resource is
            referenced by FocusOn.  For example, based on a ProcedureRequest (= BasedOn),
            a task is created to fulfil a procedureRequest ( = FocusOn ) to collect a
            specimen from a patient.

        groupIdentifier: An identifier that links together multiple tasks and other requests that were
            created in the same context.

        partOf: Task that this particular task is part of.

        status: The current status of the task.

        statusReason: An explanation as to why this task is held, failed, was refused, etc.

        businessStatus: Contains business-specific nuances of the business state.

        intent: Indicates the "level" of actionability associated with the Task.  I.e. Is this
            a proposed task, a planned task, an actionable task, etc.

        priority: Indicates how quickly the Task should be addressed with respect to other
            requests.

        code: A name or code (or both) briefly describing what the task involves.

        description: A free-text description of what is to be performed.

        focus: The request being actioned or the resource being manipulated by this task.

        for: The entity who benefits from the performance of the service specified in the
            task (e.g., the patient).

        context: The healthcare event  (e.g. a patient and healthcare provider interaction)
            during which this task was created.

        executionPeriod: Identifies the time action was first taken against the task (start) and/or the
            time final action was taken against the task prior to marking it as completed
            (end).

        authoredOn: The date and time this task was created.

        lastModified: The date and time of last modification to this task.

        requester: The creator of the task.

        performerType: The type of participant that can execute the task.

        owner: Individual organization or Device currently responsible for task execution.

        reason: A description or code indicating why this task needs to be performed.

        note: Free-text information captured about the task as it progresses.

        relevantHistory: Links to Provenance records for past versions of this Task that identify key
            state transitions or updates that are likely to be relevant to a user looking
            at the current version of the task.

        restriction: If the Task.focus is a request resource and the task is seeking fulfillment
            (i.e is asking for the request to be actioned), this element identifies any
            limitations on what parts of the referenced request should be actioned.

        input: Additional information that may be needed in the execution of the task.

        output: Outputs produced by the Task.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.stu3.complex_types.period import PeriodSchema
        from spark_fhir_schemas.stu3.complex_types.task_requester import Task_RequesterSchema
        from spark_fhir_schemas.stu3.complex_types.annotation import AnnotationSchema
        from spark_fhir_schemas.stu3.complex_types.task_restriction import Task_RestrictionSchema
        from spark_fhir_schemas.stu3.complex_types.task_input import Task_InputSchema
        from spark_fhir_schemas.stu3.complex_types.task_output import Task_OutputSchema
        if (
            max_recursion_limit
            and nesting_list.count("Task") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Task"]
        schema = StructType(
            [
                # This is a Task resource
                StructField("resourceType", StringType(), True),
                # The business identifier for this task.
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
                # A reference to a formal or informal definition of the task.  For example, a
                # protocol, a step within a defined workflow definition, etc.
                StructField("definitionUri", StringType(), True),
                # A reference to a formal or informal definition of the task.  For example, a
                # protocol, a step within a defined workflow definition, etc.
                StructField(
                    "definitionReference",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # BasedOn refers to a higher-level authorization that triggered the creation of
                # the task.  It references a "request" resource such as a ProcedureRequest,
                # MedicationRequest, ProcedureRequest, CarePlan, etc. which is distinct from the
                # "request" resource the task is seeking to fulfil.  This latter resource is
                # referenced by FocusOn.  For example, based on a ProcedureRequest (= BasedOn),
                # a task is created to fulfil a procedureRequest ( = FocusOn ) to collect a
                # specimen from a patient.
                StructField(
                    "basedOn",
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
                # An identifier that links together multiple tasks and other requests that were
                # created in the same context.
                StructField(
                    "groupIdentifier",
                    IdentifierSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Task that this particular task is part of.
                StructField(
                    "partOf",
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
                # The current status of the task.
                StructField("status", StringType(), True),
                # An explanation as to why this task is held, failed, was refused, etc.
                StructField(
                    "statusReason",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Contains business-specific nuances of the business state.
                StructField(
                    "businessStatus",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Indicates the "level" of actionability associated with the Task.  I.e. Is this
                # a proposed task, a planned task, an actionable task, etc.
                StructField("intent", StringType(), True),
                # Indicates how quickly the Task should be addressed with respect to other
                # requests.
                StructField("priority", StringType(), True),
                # A name or code (or both) briefly describing what the task involves.
                StructField(
                    "code",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A free-text description of what is to be performed.
                StructField("description", StringType(), True),
                # The request being actioned or the resource being manipulated by this task.
                StructField(
                    "focus",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The entity who benefits from the performance of the service specified in the
                # task (e.g., the patient).
                StructField(
                    "for",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The healthcare event  (e.g. a patient and healthcare provider interaction)
                # during which this task was created.
                StructField(
                    "context",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Identifies the time action was first taken against the task (start) and/or the
                # time final action was taken against the task prior to marking it as completed
                # (end).
                StructField(
                    "executionPeriod",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The date and time this task was created.
                StructField("authoredOn", StringType(), True),
                # The date and time of last modification to this task.
                StructField("lastModified", StringType(), True),
                # The creator of the task.
                StructField(
                    "requester",
                    Task_RequesterSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The type of participant that can execute the task.
                StructField(
                    "performerType",
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
                # Individual organization or Device currently responsible for task execution.
                StructField(
                    "owner",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A description or code indicating why this task needs to be performed.
                StructField(
                    "reason",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Free-text information captured about the task as it progresses.
                StructField(
                    "note",
                    ArrayType(
                        AnnotationSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Links to Provenance records for past versions of this Task that identify key
                # state transitions or updates that are likely to be relevant to a user looking
                # at the current version of the task.
                StructField(
                    "relevantHistory",
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
                # If the Task.focus is a request resource and the task is seeking fulfillment
                # (i.e is asking for the request to be actioned), this element identifies any
                # limitations on what parts of the referenced request should be actioned.
                StructField(
                    "restriction",
                    Task_RestrictionSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Additional information that may be needed in the execution of the task.
                StructField(
                    "input",
                    ArrayType(
                        Task_InputSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Outputs produced by the Task.
                StructField(
                    "output",
                    ArrayType(
                        Task_OutputSchema.get_schema(
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
