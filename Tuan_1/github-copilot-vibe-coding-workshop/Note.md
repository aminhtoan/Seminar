// build js và build python
docker compose -f compose-js-python.yaml build --no-cache
// chạy
docker compose -f compose-js-python.yaml up


// build c# và java
docker compose -f compose.yaml build --no-cache
// chạy
docker compose -f compose.yaml up
con này nó chạy hoài ko dừng cỡ 2 3p out ra là đc rồi, tính năng đó

!!! Nhớ bật docker trc khi chạy