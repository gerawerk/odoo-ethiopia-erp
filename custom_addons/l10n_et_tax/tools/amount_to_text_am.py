# Part of Odoo. See LICENSE file for full copyright and licensing details.
"""
Ethiopian Amharic Amount-to-Words Converter
Converts monetary amounts in ETB (Ethiopian Birr) to standard Amharic text representation.
Compliant with Ministry of Revenues (MOR) financial receipts and legal voucher standards.
"""

def num_to_amharic(n):
    """Converts an integer number into Amharic words."""
    units = ['', 'አንድ', 'ሁለት', 'ሶስት', 'አራት', 'አምስት', 'ስድስት', 'ሰባት', 'ስምንት', 'ዘጠኝ']
    teens = [
        'አስር', 'አስራ አንድ', 'አስራ ሁለት', 'አስራ ሶስት', 'አስራ አራት',
        'አስራ አምስት', 'አስራ ስድስት', 'አስራ ሰባት', 'አስራ ስምንት', 'አስራ ዘጠኝ'
    ]
    tens = ['', '', 'ሀያ', 'ሰላሳ', 'አርባ', 'ሃምሳ', 'ስድሳ', 'ሰባ', 'ሰማንያ', 'ዘጠና']

    def convert_hundred(num):
        parts = []
        h = num // 100
        r = num % 100
        if h > 0:
            parts.append(f'{units[h]} መቶ')
        if 10 <= r < 20:
            parts.append(teens[r - 10])
        else:
            t = r // 10
            u = r % 10
            if t > 0:
                parts.append(tens[t])
            if u > 0:
                parts.append(units[u])
        return ' '.join(parts)

    if n == 0:
        return 'ዜሮ'

    scales = [
        (1000000000, 'ቢሊዮን'),
        (1000000, 'ሚሊዮን'),
        (1000, 'ሺህ'),
    ]

    parts = []
    rem = n
    for scale, name in scales:
        cnt = rem // scale
        if cnt > 0:
            parts.append(f'{convert_hundred(cnt)} {name}')
            rem = rem % scale

    if rem > 0:
        parts.append(convert_hundred(rem))

    return ' '.join(parts).strip()


def amount_to_amharic(amount):
    """
    Converts a monetary amount into official Amharic financial wording.
    Example:
        12500.50 -> "አስራ ሁለት ሺህ አምስት መቶ ብር ከሃምሳ ሳንቲም ብቻ"
        3000.00  -> "ሶስት ሺህ ብር ብቻ"
    """
    amount = round(float(amount or 0.0), 2)
    birr = int(amount)
    cents = int(round((amount - birr) * 100))

    if birr == 0 and cents == 0:
        return 'ዜሮ ብር ብቻ'

    parts = []
    if birr > 0:
        parts.append(f'{num_to_amharic(birr)} ብር')
    if cents > 0:
        parts.append(f'ከ{num_to_amharic(cents)} ሳንቲም')
    parts.append('ብቻ')
    return ' '.join(parts)
