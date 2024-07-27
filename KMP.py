def kmp_search(text, pattern):
    m = len(pattern)
    n = len(text)
    pi = [0] * m

    # 生成部分匹配表
    compute_prefix_function(pattern, m, pi)

    q = 0  # 模式串的索引
    i = 0  # 文本串的索引

    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q - 1]

        if pattern[q] == text[i]:
            q += 1

        if q == m:
            return True  # i - m + 1  # 返回匹配的起始索引
    return False  # -1  # 没有匹配


def compute_prefix_function(pattern, m, pi):
    k = 0
    for q in range(1, m):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k - 1]

        if pattern[k] == pattern[q]:
            k += 1

        pi[q] = k

