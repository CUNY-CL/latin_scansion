all: all.far

all.far: all.grm hexameter.far normalize.far pronounce.far syllable.far \
	     variable.far
	thraxcompiler --input_grammar=$< --output_far=$@

byte.far: byte.grm
	thraxcompiler --input_grammar=$< --output_far=$@

inventory.far: inventory.grm byte.far
	thraxcompiler --input_grammar=$< --output_far=$@

foot.far: foot.grm
	thraxcompiler --input_grammar=$< --output_far=$@

hexameter.far: hexameter.grm byte.far foot.far syllable.far utility.far \
	           weight.far
	thraxcompiler --input_grammar=$< --output_far=$@

normalize.far: normalize.grm byte.far
	thraxcompiler --input_grammar=$< --output_far=$@

pronounce.far: pronounce.grm byte.far inventory.far utility.far
	thraxcompiler --input_grammar=$< --output_far=$@

syllable.far: syllable.grm byte.far inventory.far utility.far
	thraxcompiler --input_grammar=$< --output_far=$@

utility.far: utility.grm inventory.far
	thraxcompiler --input_grammar=$< --output_far=$@

variable.far: variable.grm byte.far inventory.far utility.far
	thraxcompiler --input_grammar=$< --output_far=$@

weight.far: weight.grm utility.far
	thraxcompiler --input_grammar=$< --output_far=$@

clean:
	$(RM) byte.far inventory.far foot.far hexameter.far normalize.far \
	      pronounce.far syllable.far utility.far variable.far weight.far
