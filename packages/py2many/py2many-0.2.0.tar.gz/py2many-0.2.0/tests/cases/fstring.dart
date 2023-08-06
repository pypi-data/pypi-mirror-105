// @dart=2.9
import 'package:sprintf/sprintf.dart';

main() {
  final int a = 10;
  print(sprintf("%s", [
    "".join(["hello ", (a + 1).toString(), " world"])
  ]));
}
