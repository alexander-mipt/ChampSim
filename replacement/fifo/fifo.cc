#include <algorithm>
#include <map>
#include <vector>

#include "cache.h"

namespace FIFO
{
constexpr uint64_t SET_LIMIT = 4096;
using SetIdx = uint32_t;
struct FifoIdx {
  SetIdx idx{0};
  bool increment{false};
};
// using FifoIdx = std::pair<bool, SetIdx>;
using SetOfFifoIdxs = std::array<FifoIdx, SET_LIMIT>;
std::map<CACHE*, SetOfFifoIdxs> FIFO{};
} // namespace FIFO

void CACHE::initialize_replacement()
{
  assert(NUM_SET <= FIFO::SET_LIMIT);
  FIFO::FIFO[this] = FIFO::SetOfFifoIdxs{};
}

uint32_t CACHE::find_victim(uint32_t triggering_cpu, uint64_t instr_id, uint32_t set, const BLOCK* current_set, uint64_t ip, uint64_t full_addr, uint32_t type)
{
  assert(set < NUM_SET);
  auto& line = FIFO::FIFO[this][set];
  FIFO::SetIdx& idx = line.idx;
  // if miss
  if (line.increment) {
    idx = (idx + 1) % NUM_SET;
  }
  return idx;
}

void CACHE::update_replacement_state(uint32_t triggering_cpu, uint32_t set, uint32_t way, uint64_t full_addr, uint64_t ip, uint64_t victim_addr, uint32_t type,
                                     uint8_t hit)
{
  bool increment{false};
  // Mark the way as being used on the current cycle
  if (!hit || type != WRITE) { // Skip this for writeback hits
    increment = true;
  }
  FIFO::FIFO[this].at(set).increment = increment;
}

void CACHE::replacement_final_stats() {}
