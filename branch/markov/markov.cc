#include <climits>
#include <map>
#include <random>

#include "msl/fwcounter.h"
#include "ooo_cpu.h"
#include <type_traits>

namespace markov
{
constexpr std::size_t TABLE_SIZE = 16384;
constexpr std::size_t PRIME = 16381;
constexpr std::size_t HIST_LENGTH = 2;
struct FreqCounters {
  uint64_t takenBranches{1};
  uint64_t notTakenBranches{1};
};

std::map<O3_CPU*, std::array<FreqCounters, TABLE_SIZE>> table;

#ifdef MARKOV_PREDICTOR_PROP_ENABLE
class Randomizer
{
public:
  Randomizer(long seed = 1) : m_distr(1, 100), m_gen(seed) {}
  unsigned get() { return m_distr(m_gen); }
  bool indicator(unsigned propability) { return get() <= propability; }

private:
  std::uniform_int_distribution<unsigned> m_distr;
  std::mt19937 m_gen;
} generator;
#endif

} // namespace markov

void O3_CPU::initialize_branch_predictor()
{
  std::cout << "CPU " << cpu << " Markov branch predictor" << std::endl;
#ifdef MARKOV_PREDICTOR_PROP_ENABLE
  std::cout << "Propability mode enabled" << std::endl;
#else
  std::cout << "Maximum value mode enabled" << std::endl;
#endif
}

uint8_t O3_CPU::predict_branch(uint64_t ip)
{
  auto hash = ip % markov::PRIME;
  const auto& value = markov::table[this][hash];
#ifndef MARKOV_PREDICTOR_PROP_ENABLE
  return value.takenBranches >= value.notTakenBranches;
#else
  unsigned takenProp = value.takenBranches * 100 / (value.takenBranches + value.notTakenBranches);
  return markov::generator.indicator(takenProp);
#endif
}

void O3_CPU::last_branch_result(uint64_t ip, uint64_t branch_target, uint8_t taken, uint8_t branch_type)
{
  auto hash = ip % markov::PRIME;
  auto& counters = markov::table[this][hash];
  if (taken) {
    counters.takenBranches += 1;
  } else {
    counters.notTakenBranches += 1;
  }
}
