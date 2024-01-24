////////////////////////////////////////////////////////////////////////////
// This file is part of 'simd-function'
////////////////////////////////////////////////////////////////////////////

#include <iostream>
#include <cstdint>
#include <vector>
#include <format>
#include <cassert>
#include <numeric>
#include <chrono>

static constexpr uint64_t VAR_TRUTH_TABLE[] = {
	0xAAAAAAAAAAAAAAAAULL, 0xCCCCCCCCCCCCCCCCULL,
	0xF0F0F0F0F0F0F0F0ULL, 0xFF00FF00FF00FF00ULL,
	0xFFFF0000FFFF0000ULL, 0xFFFFFFFF00000000ULL
};

// Functions to optimize against
static constexpr uint64_t xor_op(uint64_t a, uint64_t b) noexcept { return a ^ b; }
static constexpr uint64_t and_op(uint64_t a, uint64_t b) noexcept { return a & b; }
static constexpr uint64_t andn_op(uint64_t a, uint64_t b) noexcept { return a & (~b); }
static constexpr uint64_t or_op(uint64_t a, uint64_t b) noexcept { return a | b; }

typedef uint64_t (*binary_op_t)(uint64_t, uint64_t);
static constexpr binary_op_t binary_op[] = { xor_op, and_op, or_op, andn_op };
static bool is_binary_op_symetric[std::size(binary_op)];
static const std::string operation_name[] = {"NOT", "XOR", "AND", "OR", "ANDN"};

struct operation {
	uint32_t op_index;
	uint32_t var0_index;
	uint32_t var1_index;

	operation(uint32_t op_index, uint32_t var0_index, uint32_t var1_index) noexcept : op_index(op_index), var0_index(var0_index), var1_index(var1_index)
	{}
	operation() noexcept : op_index(0), var0_index(0), var1_index(0)
	{}
};
static bool operator==(const operation& op1, const operation& op2) noexcept
{
	return op1.op_index == op2.op_index && op1.var0_index == op2.var0_index && op1.var1_index == op2.var1_index;
}
static std::vector<std::vector<operation>> found;
static operation my_operations[32];
static uint32_t num_operations = 0;

// Boolen Function to optimize
//static constexpr uint64_t function_truth_table = ((VAR_TRUTH_TABLE[0] & (VAR_TRUTH_TABLE[1] | VAR_TRUTH_TABLE[2])) | (VAR_TRUTH_TABLE[1] & VAR_TRUTH_TABLE[2]));
static constexpr uint64_t function_truth_tables[] = {
	//(VAR_TRUTH_TABLE[2] ^ (VAR_TRUTH_TABLE[0] & (VAR_TRUTH_TABLE[1] ^ VAR_TRUTH_TABLE[2]))),
	//(VAR_TRUTH_TABLE[1] ^ (VAR_TRUTH_TABLE[3] & (VAR_TRUTH_TABLE[0] ^ VAR_TRUTH_TABLE[1])))
	((VAR_TRUTH_TABLE[0] & (VAR_TRUTH_TABLE[1] | VAR_TRUTH_TABLE[2])) | (VAR_TRUTH_TABLE[1] & VAR_TRUTH_TABLE[2])),
	((VAR_TRUTH_TABLE[3] & (VAR_TRUTH_TABLE[0] | VAR_TRUTH_TABLE[1])) | (VAR_TRUTH_TABLE[0] & VAR_TRUTH_TABLE[1]))
};
static constexpr uint32_t num_function_params = 4;// 3;
static uint32_t max_function_depth = 6;//3;
static constexpr uint32_t VALUE_FOUND_MASK = ~(UINT32_MAX << std::size(function_truth_tables));

static std::chrono::time_point<std::chrono::steady_clock> start;

static void recursive_optimize(uint32_t depth, uint32_t vars_index, uint32_t value_found, uint64_t vars[32]) noexcept
{
	// Check if value found
	for (size_t j = 0; j < std::size(function_truth_tables); j++)
		if (vars[vars_index - 1] == function_truth_tables[j])
			value_found |= 1 << j;

	if (value_found == VALUE_FOUND_MASK)// All outputs found
	{
		if (depth < max_function_depth)
			max_function_depth = depth;

		// Create the operations
		std::vector<operation> operations;
		for (uint32_t i = 0; i < num_operations; i++)
			operations.push_back(my_operations[i]);
		found.push_back(std::move(operations));
		return;
	}

	if (depth >= max_function_depth) return;

	// Unary operation => not
	for (uint32_t i = 0; i < vars_index; i++)
	{
		my_operations[num_operations] = operation(0, i, -1);
		num_operations++;
		vars[vars_index] = ~vars[i];
		recursive_optimize(depth + 1, vars_index + 1, value_found, vars);
		num_operations--;
	}
	if (depth == 0)
	{
		auto duration = std::chrono::duration_cast<std::chrono::seconds>(std::chrono::high_resolution_clock::now() - start);
		std::cout << std::format("Completion {:3}% {:02}:{:02}\n", 100 / (std::size(binary_op) + 1), duration.count() / 60, duration.count() % 60);
	}
	// Binary operation
	for (uint32_t op_index = 0; op_index < std::size(binary_op); op_index++)
	{
		if (is_binary_op_symetric[op_index])
		{
			for (uint32_t i = 0; i < vars_index; i++)
				// Use symetry for symetric boolean operators
				for (uint32_t j = i + 1; j < vars_index; j++)
				{
					my_operations[num_operations] = operation(op_index + 1, i, j);
					num_operations++;
					vars[vars_index] = binary_op[op_index](vars[i], vars[j]);
					recursive_optimize(depth + 1, vars_index + 1, value_found, vars);
					num_operations--;
				}
		}
		else
		{
			for (uint32_t i = 0; i < vars_index; i++)
				// Use symetry for symetric boolean operators
				for (uint32_t j = 0; j < vars_index; j++)
				{
					my_operations[num_operations] = operation(op_index + 1, i, j);
					num_operations++;
					vars[vars_index] = binary_op[op_index](vars[i], vars[j]);
					recursive_optimize(depth + 1, vars_index + 1, value_found, vars);
					num_operations--;
				}
		}

		if (depth == 0)
		{
			auto duration = std::chrono::duration_cast<std::chrono::seconds>(std::chrono::high_resolution_clock::now() - start);
			std::cout << std::format("Completion {:3}% {:02}:{:02}\n", 100 * (op_index + 2) / (std::size(binary_op) + 1), duration.count() / 60, duration.count() % 60);
		}
	}
}

static uint32_t count_tmp_registers(const std::vector<operation>& solution, uint32_t op_index) noexcept
{
	uint32_t var0_count = 0, var1_count = 0;

	if (solution[op_index].var0_index >= num_function_params && solution[op_index].var0_index < (max_function_depth + num_function_params - 1))
		var0_count = std::max(1u, count_tmp_registers(solution, solution[op_index].var0_index - num_function_params));

	if (solution[op_index].var1_index >= num_function_params && solution[op_index].var1_index < (max_function_depth + num_function_params - 1))
		var1_count = std::max(1u, count_tmp_registers(solution, solution[op_index].var1_index - num_function_params));

	return var0_count + var1_count;
}
static std::string print_expresion(const std::vector<operation>& solution, uint32_t op_index) noexcept
{
	std::string var0, var1;

	if (solution[op_index].var0_index >= num_function_params && solution[op_index].var0_index < (max_function_depth + num_function_params - 1))
		var0 = print_expresion(solution, solution[op_index].var0_index - num_function_params);
	else
		var0 = std::format("x{}", solution[op_index].var0_index);

	if (solution[op_index].var1_index >= num_function_params && solution[op_index].var1_index < (max_function_depth + num_function_params - 1))
		var1 = print_expresion(solution, solution[op_index].var1_index - num_function_params);
	else
		var1 = std::format("x{}", solution[op_index].var1_index);

	if (operation_name[solution[op_index].op_index] == "XOR")
		return std::format("({} ^ {})", var0, var1);
	else if (operation_name[solution[op_index].op_index] == "OR")
		return std::format("({} | {})", var0, var1);
	else if (operation_name[solution[op_index].op_index] == "AND")
		return std::format("({} & {})", var0, var1);
	else
		return std::format("{}({}, {})", operation_name[solution[op_index].op_index],  var0, var1);
}

static void optimize() noexcept
{
	// Initialize variables
	uint64_t vars[32];
	for (uint32_t i = 0; i < num_function_params; i++)
		vars[i] = VAR_TRUTH_TABLE[i];
	// Are binary operations symetric?
	for (size_t i = 0; i < std::size(binary_op); i++)
		is_binary_op_symetric[i] = binary_op[i](VAR_TRUTH_TABLE[0], VAR_TRUTH_TABLE[1]) == binary_op[i](VAR_TRUTH_TABLE[1], VAR_TRUTH_TABLE[0]);

	// Optimize
	num_operations = 0;
	recursive_optimize(0, num_function_params, 0, vars);

	// Delete repeated solutions
	std::vector<bool> good_solution(found.size(), true);
	for (size_t i = 0; i < found.size(); i++)
	{
		if (found[i].size() > max_function_depth)
		{
			good_solution[i] = false;
			continue;
		}

		for (size_t j = i + 1; j < found.size(); j++)
		{
			assert(found[i].size() == found[j].size());

			uint32_t op_found = 0;
			for (const auto& op0 : found[i])
				for (const auto& op1 : found[j])
					if (op0 == op1)
					{
						op_found++;
						break;
					}

			if (op_found == found[j].size())
				good_solution[j] = false;
		}
	}

	//int s = std::accumulate(good_solution.cbegin(), good_solution.cend(), 0);
	// Show
	for (size_t i = 0; i < found.size(); i++)
		if (good_solution[i])
		{
			//for (const auto& op : found[i])
				std::cout << print_expresion(found[i], static_cast<uint32_t>(found[i].size() - 1));//std::format("{}({}, {})\n", operation_name[op.op_index], op.var0_index, op.var1_index);

			std::cout << std::format("\nNumTmpRegs = {}\n\n", count_tmp_registers(found[i], static_cast<uint32_t>(found[i].size() - 1)));
		}
}

int main()
{
	std::cout << "Begin optimization\n";
	start = std::chrono::high_resolution_clock::now();
	optimize();
	std::cout << "End optimization\n";

	return 0;
}