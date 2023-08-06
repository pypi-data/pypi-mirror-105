// @dart=2.9
import 'dart:math';
import 'package:sprintf/sprintf.dart';
import 'package:tuple/tuple.dart';

List<int> comb_sort(List<int> seq) {
  var gap = seq.length;
  bool swap = true;
  while (gap > 1 || swap) {
    gap = max(1, (gap / 1.25).floor());
    swap = false;
    for (final i in ([for (var i = 0; i < (seq.length - gap); i += 1) i])) {
      if (seq[i] > seq[(i + gap)]) {
        final __tmp1 = Tuple2<int, int>(seq[(i + gap)], seq[i]);
        seq[i] = __tmp1.item1;
        seq[(i + gap)] = __tmp1.item2;
        swap = true;
      }
    }
  }
  return seq;
}

main() {
  var unsorted = [14, 11, 19, 5, 16, 10, 19, 12, 5, 12];
  final expected = [5, 5, 10, 11, 12, 12, 14, 16, 19, 19];
  assert(comb_sort(unsorted) == expected);
  print(sprintf("%s", ["OK"]));
}
