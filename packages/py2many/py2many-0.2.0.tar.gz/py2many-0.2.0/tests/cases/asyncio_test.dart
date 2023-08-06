// @dart=2.9
import 'package:sprintf/sprintf.dart';
#[async]
int nested() {
return 42;}


#[async]
 async_main() {
assert(await!(nested()) == 42);
print(sprintf("%s", ["OK"]));}


 main() {
asyncio.run(async_main());}


