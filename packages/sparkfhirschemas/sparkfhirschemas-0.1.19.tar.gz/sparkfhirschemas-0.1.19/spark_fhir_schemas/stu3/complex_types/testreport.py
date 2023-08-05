from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import DataType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class TestReportSchema:
    """
    A summary of information based on the results of executing a TestScript.
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
        A summary of information based on the results of executing a TestScript.


        resourceType: This is a TestReport resource

        identifier: Identifier for the TestScript assigned for external purposes outside the
            context of FHIR.

        name: A free text natural language name identifying the executed TestScript.

        status: The current state of this test report.

        testScript: Ideally this is an absolute URL that is used to identify the version-specific
            TestScript that was executed, matching the `TestScript.url`.

        result: The overall result from the execution of the TestScript.

        score: The final score (percentage of tests passed) resulting from the execution of
            the TestScript.

        tester: Name of the tester producing this report (Organization or individual).

        issued: When the TestScript was executed and this TestReport was generated.

        participant: A participant in the test execution, either the execution engine, a client, or
            a server.

        setup: The results of the series of required setup operations before the tests were
            executed.

        test: A test executed from the test script.

        teardown: The results of the series of operations required to clean up after the all the
            tests were executed (successfully or otherwise).

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.testreport_participant import TestReport_ParticipantSchema
        from spark_fhir_schemas.stu3.complex_types.testreport_setup import TestReport_SetupSchema
        from spark_fhir_schemas.stu3.complex_types.testreport_test import TestReport_TestSchema
        from spark_fhir_schemas.stu3.complex_types.testreport_teardown import TestReport_TeardownSchema
        if (
            max_recursion_limit
            and nesting_list.count("TestReport") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["TestReport"]
        schema = StructType(
            [
                # This is a TestReport resource
                StructField("resourceType", StringType(), True),
                # Identifier for the TestScript assigned for external purposes outside the
                # context of FHIR.
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
                # A free text natural language name identifying the executed TestScript.
                StructField("name", StringType(), True),
                # The current state of this test report.
                StructField("status", StringType(), True),
                # Ideally this is an absolute URL that is used to identify the version-specific
                # TestScript that was executed, matching the `TestScript.url`.
                StructField(
                    "testScript",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The overall result from the execution of the TestScript.
                StructField("result", StringType(), True),
                # The final score (percentage of tests passed) resulting from the execution of
                # the TestScript.
                StructField("score", IntegerType(), True),
                # Name of the tester producing this report (Organization or individual).
                StructField("tester", StringType(), True),
                # When the TestScript was executed and this TestReport was generated.
                StructField("issued", StringType(), True),
                # A participant in the test execution, either the execution engine, a client, or
                # a server.
                StructField(
                    "participant",
                    ArrayType(
                        TestReport_ParticipantSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # The results of the series of required setup operations before the tests were
                # executed.
                StructField(
                    "setup",
                    TestReport_SetupSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A test executed from the test script.
                StructField(
                    "test",
                    ArrayType(
                        TestReport_TestSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # The results of the series of operations required to clean up after the all the
                # tests were executed (successfully or otherwise).
                StructField(
                    "teardown",
                    TestReport_TeardownSchema.get_schema(
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
