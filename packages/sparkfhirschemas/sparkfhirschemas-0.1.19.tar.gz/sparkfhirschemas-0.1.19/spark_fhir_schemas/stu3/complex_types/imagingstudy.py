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
class ImagingStudySchema:
    """
    Representation of the content produced in a DICOM imaging study. A study
    comprises a set of series, each of which includes a set of Service-Object Pair
    Instances (SOP Instances - images or other data) acquired or produced in a
    common context.  A series is of only one modality (e.g. X-ray, CT, MR,
    ultrasound), but a study may have multiple series of different modalities.
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
        Representation of the content produced in a DICOM imaging study. A study
        comprises a set of series, each of which includes a set of Service-Object Pair
        Instances (SOP Instances - images or other data) acquired or produced in a
        common context.  A series is of only one modality (e.g. X-ray, CT, MR,
        ultrasound), but a study may have multiple series of different modalities.


        resourceType: This is a ImagingStudy resource

        uid: Formal identifier for the study.

        accession: Accession Number is an identifier related to some aspect of imaging workflow
            and data management. Usage may vary across different institutions.  See for
            instance [IHE Radiology Technical Framework Volume 1 Appendix A](http://www.ih
            e.net/uploadedFiles/Documents/Radiology/IHE_RAD_TF_Rev13.0_Vol1_FT_2014-07-30.
            pdf).

        identifier: Other identifiers for the study.

        availability: Availability of study (online, offline, or nearline).

        modalityList: A list of all the Series.ImageModality values that are actual acquisition
            modalities, i.e. those in the DICOM Context Group 29 (value set OID
            1.2.840.10008.6.1.19).

        patient: The patient imaged in the study.

        context: The encounter or episode at which the request is initiated.

        started: Date and time the study started.

        basedOn: A list of the diagnostic requests that resulted in this imaging study being
            performed.

        referrer: The requesting/referring physician.

        interpreter: Who read the study and interpreted the images or other content.

        endpoint: The network service providing access (e.g., query, view, or retrieval) for the
            study. See implementation notes for information about using DICOM endpoints. A
            study-level endpoint applies to each series in the study, unless overridden by
            a series-level endpoint with the same Endpoint.type.

        numberOfSeries: Number of Series in the Study. This value given may be larger than the number
            of series elements this Resource contains due to resource availability,
            security, or other factors. This element should be present if any series
            elements are present.

        numberOfInstances: Number of SOP Instances in Study. This value given may be larger than the
            number of instance elements this resource contains due to resource
            availability, security, or other factors. This element should be present if
            any instance elements are present.

        procedureReference: A reference to the performed Procedure.

        procedureCode: The code for the performed procedure type.

        reason: Description of clinical condition indicating why the ImagingStudy was
            requested.

        description: Institution-generated description or classification of the Study performed.

        series: Each study has one or more series of images or other content.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.coding import CodingSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.stu3.complex_types.imagingstudy_series import ImagingStudy_SeriesSchema
        if (
            max_recursion_limit
            and nesting_list.count("ImagingStudy") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["ImagingStudy"]
        schema = StructType(
            [
                # This is a ImagingStudy resource
                StructField("resourceType", StringType(), True),
                # Formal identifier for the study.
                StructField("uid", StringType(), True),
                # Accession Number is an identifier related to some aspect of imaging workflow
                # and data management. Usage may vary across different institutions.  See for
                # instance [IHE Radiology Technical Framework Volume 1 Appendix A](http://www.ih
                # e.net/uploadedFiles/Documents/Radiology/IHE_RAD_TF_Rev13.0_Vol1_FT_2014-07-30.
                # pdf).
                StructField(
                    "accession",
                    IdentifierSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Other identifiers for the study.
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
                # Availability of study (online, offline, or nearline).
                StructField("availability", StringType(), True),
                # A list of all the Series.ImageModality values that are actual acquisition
                # modalities, i.e. those in the DICOM Context Group 29 (value set OID
                # 1.2.840.10008.6.1.19).
                StructField(
                    "modalityList",
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
                # The patient imaged in the study.
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
                # The encounter or episode at which the request is initiated.
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
                # Date and time the study started.
                StructField("started", StringType(), True),
                # A list of the diagnostic requests that resulted in this imaging study being
                # performed.
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
                # The requesting/referring physician.
                StructField(
                    "referrer",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Who read the study and interpreted the images or other content.
                StructField(
                    "interpreter",
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
                # The network service providing access (e.g., query, view, or retrieval) for the
                # study. See implementation notes for information about using DICOM endpoints. A
                # study-level endpoint applies to each series in the study, unless overridden by
                # a series-level endpoint with the same Endpoint.type.
                StructField(
                    "endpoint",
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
                # Number of Series in the Study. This value given may be larger than the number
                # of series elements this Resource contains due to resource availability,
                # security, or other factors. This element should be present if any series
                # elements are present.
                StructField("numberOfSeries", IntegerType(), True),
                # Number of SOP Instances in Study. This value given may be larger than the
                # number of instance elements this resource contains due to resource
                # availability, security, or other factors. This element should be present if
                # any instance elements are present.
                StructField("numberOfInstances", IntegerType(), True),
                # A reference to the performed Procedure.
                StructField(
                    "procedureReference",
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
                # The code for the performed procedure type.
                StructField(
                    "procedureCode",
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
                # Description of clinical condition indicating why the ImagingStudy was
                # requested.
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
                # Institution-generated description or classification of the Study performed.
                StructField("description", StringType(), True),
                # Each study has one or more series of images or other content.
                StructField(
                    "series",
                    ArrayType(
                        ImagingStudy_SeriesSchema.get_schema(
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
