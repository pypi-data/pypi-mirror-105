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
class DeviceMetricSchema:
    """
    Describes a measurement, calculation or setting capability of a medical
    device.
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
        Describes a measurement, calculation or setting capability of a medical
        device.


        resourceType: This is a DeviceMetric resource

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

        identifier: Unique instance identifiers assigned to a device by the device or gateway
            software, manufacturers, other organizations or owners. For example: handle
            ID.

        type: Describes the type of the metric. For example: Heart Rate, PEEP Setting, etc.

        unit: Describes the unit that an observed value determined for this metric will
            have. For example: Percent, Seconds, etc.

        source: Describes the link to the  Device that this DeviceMetric belongs to and that
            contains administrative device information such as manufacturer, serial
            number, etc.

        parent: Describes the link to the  Device that this DeviceMetric belongs to and that
            provide information about the location of this DeviceMetric in the containment
            structure of the parent Device. An example would be a Device that represents a
            Channel. This reference can be used by a client application to distinguish
            DeviceMetrics that have the same type, but should be interpreted based on
            their containment location.

        operationalStatus: Indicates current operational state of the device. For example: On, Off,
            Standby, etc.

        color: Describes the color representation for the metric. This is often used to aid
            clinicians to track and identify parameter types by color. In practice,
            consider a Patient Monitor that has ECG/HR and Pleth for example; the
            parameters are displayed in different characteristic colors, such as HR-blue,
            BP-green, and PR and SpO2- magenta.

        category: Indicates the category of the observation generation process. A DeviceMetric
            can be for example a setting, measurement, or calculation.

        measurementPeriod: Describes the measurement repetition time. This is not necessarily the same as
            the update period. The measurement repetition time can range from milliseconds
            up to hours. An example for a measurement repetition time in the range of
            milliseconds is the sampling rate of an ECG. An example for a measurement
            repetition time in the range of hours is a NIBP that is triggered
            automatically every hour. The update period may be different than the
            measurement repetition time, if the device does not update the published
            observed value with the same frequency as it was measured.

        calibration: Describes the calibrations that have been performed or that are required to be
            performed.

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
        from spark_fhir_schemas.r4.complex_types.timing import TimingSchema
        from spark_fhir_schemas.r4.complex_types.devicemetric_calibration import DeviceMetric_CalibrationSchema
        if (
            max_recursion_limit
            and nesting_list.count("DeviceMetric") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["DeviceMetric"]
        schema = StructType(
            [
                # This is a DeviceMetric resource
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
                # Unique instance identifiers assigned to a device by the device or gateway
                # software, manufacturers, other organizations or owners. For example: handle
                # ID.
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
                # Describes the type of the metric. For example: Heart Rate, PEEP Setting, etc.
                StructField(
                    "type",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Describes the unit that an observed value determined for this metric will
                # have. For example: Percent, Seconds, etc.
                StructField(
                    "unit",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Describes the link to the  Device that this DeviceMetric belongs to and that
                # contains administrative device information such as manufacturer, serial
                # number, etc.
                StructField(
                    "source",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Describes the link to the  Device that this DeviceMetric belongs to and that
                # provide information about the location of this DeviceMetric in the containment
                # structure of the parent Device. An example would be a Device that represents a
                # Channel. This reference can be used by a client application to distinguish
                # DeviceMetrics that have the same type, but should be interpreted based on
                # their containment location.
                StructField(
                    "parent",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Indicates current operational state of the device. For example: On, Off,
                # Standby, etc.
                StructField("operationalStatus", StringType(), True),
                # Describes the color representation for the metric. This is often used to aid
                # clinicians to track and identify parameter types by color. In practice,
                # consider a Patient Monitor that has ECG/HR and Pleth for example; the
                # parameters are displayed in different characteristic colors, such as HR-blue,
                # BP-green, and PR and SpO2- magenta.
                StructField("color", StringType(), True),
                # Indicates the category of the observation generation process. A DeviceMetric
                # can be for example a setting, measurement, or calculation.
                StructField("category", StringType(), True),
                # Describes the measurement repetition time. This is not necessarily the same as
                # the update period. The measurement repetition time can range from milliseconds
                # up to hours. An example for a measurement repetition time in the range of
                # milliseconds is the sampling rate of an ECG. An example for a measurement
                # repetition time in the range of hours is a NIBP that is triggered
                # automatically every hour. The update period may be different than the
                # measurement repetition time, if the device does not update the published
                # observed value with the same frequency as it was measured.
                StructField(
                    "measurementPeriod",
                    TimingSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Describes the calibrations that have been performed or that are required to be
                # performed.
                StructField(
                    "calibration",
                    ArrayType(
                        DeviceMetric_CalibrationSchema.get_schema(
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
