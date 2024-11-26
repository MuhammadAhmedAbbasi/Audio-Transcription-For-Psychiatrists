from Service.common.data.word_mapping_pointer import WordMappingPointer
# Function for word mapping
async def word_mapping(old_sentence_list,new_senetence_list):
    matched_word_length = await longest_consecutive_common_subsequence(old_sentence_list, new_senetence_list)
    for i in range(len(old_sentence_list) - matched_word_length+1):
        chunk_data_2 = old_sentence_list[i : i + matched_word_length]
        for j in range(len(new_senetence_list) - matched_word_length+1):
            chunk_data_3 = new_senetence_list[j : j + matched_word_length]
            if chunk_data_2 == chunk_data_3:
                old_chunk_unmapped_pointer = len(old_sentence_list[:i])
                new_chunk_unmapped_pointer =  len(new_senetence_list[:j]) 
                return WordMappingPointer(old_chunk_unmapped_pointer = old_chunk_unmapped_pointer,
                                           new_chunk_unmapped_pointer = new_chunk_unmapped_pointer)
                # return old_chunk_unmapped_pointer, new_chunk_unmapped_pointer

# Function for finding the longest consecutive match
async def longest_consecutive_common_subsequence(old, new) ->int:
    m, n = len(old), len(new)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_length = 0
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if old[i - 1] == new[j - 1]:  # If elements match
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_length:  # Update maximum length
                    max_length = dp[i][j]
            else:
                dp[i][j] = 0  # No common substring here
    return max_length 
