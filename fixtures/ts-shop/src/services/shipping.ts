/**
 * Shipping rate lookups.
 *
 * CONTROL: HTTP call with timeout, retry (via p-retry), and logged catch
 *          → handled for timeout, server_error, rate_limited
 */
import axios from "axios";
import pRetry from "p-retry";

const client = axios.create({
  baseURL: "https://api.shipping-provider.com/v1",
  timeout: 10000,
});

export async function getRates(originZip: string, destZip: string, weightKg: number) {
  return pRetry(
    async () => {
      try {
        const resp = await client.post("/rates", {
          origin: originZip,
          dest: destZip,
          weight: weightKg,
        });
        return resp.data.rates;
      } catch (err: any) {
        console.error("Shipping API error:", err.message);
        throw err;
      }
    },
    { retries: 3 }
  );
}
