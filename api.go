package main

import (
  "bytes"
  "encoding/json"
  "log"
  "net/http"
)

func main() {
  data := []byte("Энд алдаатаай бичвэрр байна.")

  req, _ := http.NewRequest(
    "POST",
    "https://api.bolor.net/v1.2/spell-check",
    bytes.NewBuffer(data))

  req.Header.Set("Content-Type", "text/plain")
  req.Header.Set("token", "{0043528da56f563301cf150c45435b10357ece7c91b2cb4873235840f03ec0ea}")

  client := &http.Client{}

  resp, err := client.Do(req)
  if err != nil {
    log.Fatal(err)
  }
  defer resp.Body.Close()

  var incorrects []string
  if err := json.NewDecoder(resp.Body).Decode(&incorrects); err != nil {
    log.Fatal(err)
  }

  log.Println(incorrects)
}
