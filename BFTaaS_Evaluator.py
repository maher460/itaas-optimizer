import benchmark_evaluation_sm1_CDFs_CSVs
import benchmark_evaluation_sm1_linegraphs
import benchmark_evaluation_sm1_barcharts
import benchmark_evaluation_sm2_CDFs_CSVs
import benchmark_evaluation_sm2_linegraphs
import benchmark_evaluation_sm2_barcharts
import benchmark_evaluation_sm3_CDFs_CSVs
import benchmark_evaluation_sm3_linegraphs
import benchmark_evaluation_sm3_barcharts


def run():

	# Service Model 1
	print("\n[BFTaaS Evaluator] Evaluating service model 1 ...\n")
	benchmark_evaluation_sm1_CDFs_CSVs.run()
	benchmark_evaluation_sm1_linegraphs.run()
	benchmark_evaluation_sm1_barcharts.run()

	print("\n[BFTaaS Evaluator] Evaluating service model 2 ...\n")
	# Service Model 2
	benchmark_evaluation_sm2_CDFs_CSVs.run()
	benchmark_evaluation_sm2_linegraphs.run()
	benchmark_evaluation_sm2_barcharts.run()

	print("\n[BFTaaS Evaluator] Evaluating service model 3 ...\n")
	# Service Model 3
	benchmark_evaluation_sm3_CDFs_CSVs.run()
	benchmark_evaluation_sm3_linegraphs.run()
	benchmark_evaluation_sm3_barcharts.run()

	print("\n[BFTaaS Evaluator] All done! Check 'evaluation_results' directory for results.\n")

run()