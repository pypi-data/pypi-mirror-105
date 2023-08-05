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
class SequenceSchema:
    """
    Raw data describing a biological sequence.
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
        Raw data describing a biological sequence.


        resourceType: This is a Sequence resource

        identifier: A unique identifier for this particular sequence instance. This is a FHIR-
            defined id.

        type: Amino Acid Sequence/ DNA Sequence / RNA Sequence.

        coordinateSystem: Whether the sequence is numbered starting at 0 (0-based numbering or
            coordinates, inclusive start, exclusive end) or starting at 1 (1-based
            numbering, inclusive start and inclusive end).

        patient: The patient whose sequencing results are described by this resource.

        specimen: Specimen used for sequencing.

        device: The method for sequencing, for example, chip information.

        performer: The organization or lab that should be responsible for this result.

        quantity: The number of copies of the seqeunce of interest. (RNASeq).

        referenceSeq: A sequence that is used as a reference to describe variants that are present
            in a sequence analyzed.

        variant: The definition of variant here originates from Sequence ontology ([variant_of]
            (http://www.sequenceontology.org/browser/current_svn/term/variant_of)). This
            element can represent amino acid or nucleic sequence change(including
            insertion,deletion,SNP,etc.)  It can represent some complex mutation or
            segment variation with the assist of CIGAR string.

        observedSeq: Sequence that was observed. It is the result marked by referenceSeq along with
            variant records on referenceSeq. This shall starts from
            referenceSeq.windowStart and end by referenceSeq.windowEnd.

        quality: An experimental feature attribute that defines the quality of the feature in a
            quantitative way, such as a phred quality score ([SO:0001686](http://www.seque
            nceontology.org/browser/current_svn/term/SO:0001686)).

        readCoverage: Coverage (read depth or depth) is the average number of reads representing a
            given nucleotide in the reconstructed sequence.

        repository: Configurations of the external repository. The repository shall store target's
            observedSeq or records related with target's observedSeq.

        pointer: Pointer to next atomic sequence which at most contains one variant.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.quantity import QuantitySchema
        from spark_fhir_schemas.stu3.complex_types.sequence_referenceseq import Sequence_ReferenceSeqSchema
        from spark_fhir_schemas.stu3.complex_types.sequence_variant import Sequence_VariantSchema
        from spark_fhir_schemas.stu3.complex_types.sequence_quality import Sequence_QualitySchema
        from spark_fhir_schemas.stu3.complex_types.sequence_repository import Sequence_RepositorySchema
        if (
            max_recursion_limit
            and nesting_list.count("Sequence") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Sequence"]
        schema = StructType(
            [
                # This is a Sequence resource
                StructField("resourceType", StringType(), True),
                # A unique identifier for this particular sequence instance. This is a FHIR-
                # defined id.
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
                # Amino Acid Sequence/ DNA Sequence / RNA Sequence.
                StructField("type", StringType(), True),
                # Whether the sequence is numbered starting at 0 (0-based numbering or
                # coordinates, inclusive start, exclusive end) or starting at 1 (1-based
                # numbering, inclusive start and inclusive end).
                StructField("coordinateSystem", IntegerType(), True),
                # The patient whose sequencing results are described by this resource.
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
                # Specimen used for sequencing.
                StructField(
                    "specimen",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The method for sequencing, for example, chip information.
                StructField(
                    "device",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The organization or lab that should be responsible for this result.
                StructField(
                    "performer",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The number of copies of the seqeunce of interest. (RNASeq).
                StructField(
                    "quantity",
                    QuantitySchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A sequence that is used as a reference to describe variants that are present
                # in a sequence analyzed.
                StructField(
                    "referenceSeq",
                    Sequence_ReferenceSeqSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The definition of variant here originates from Sequence ontology ([variant_of]
                # (http://www.sequenceontology.org/browser/current_svn/term/variant_of)). This
                # element can represent amino acid or nucleic sequence change(including
                # insertion,deletion,SNP,etc.)  It can represent some complex mutation or
                # segment variation with the assist of CIGAR string.
                StructField(
                    "variant",
                    ArrayType(
                        Sequence_VariantSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Sequence that was observed. It is the result marked by referenceSeq along with
                # variant records on referenceSeq. This shall starts from
                # referenceSeq.windowStart and end by referenceSeq.windowEnd.
                StructField("observedSeq", StringType(), True),
                # An experimental feature attribute that defines the quality of the feature in a
                # quantitative way, such as a phred quality score ([SO:0001686](http://www.seque
                # nceontology.org/browser/current_svn/term/SO:0001686)).
                StructField(
                    "quality",
                    ArrayType(
                        Sequence_QualitySchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Coverage (read depth or depth) is the average number of reads representing a
                # given nucleotide in the reconstructed sequence.
                StructField("readCoverage", IntegerType(), True),
                # Configurations of the external repository. The repository shall store target's
                # observedSeq or records related with target's observedSeq.
                StructField(
                    "repository",
                    ArrayType(
                        Sequence_RepositorySchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Pointer to next atomic sequence which at most contains one variant.
                StructField(
                    "pointer",
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
            ]
        )
        if not include_extension:
            schema.fields = [
                c if c.name != "extension" else
                StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
