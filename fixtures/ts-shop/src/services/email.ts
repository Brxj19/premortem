/**
 * Email notifications via SendGrid.
 *
 * BUG 12: SendGrid email call catches errors, logs nothing, returns success
 *         → http_api:sendgrid / server_error / partial, detectability 5
 */
import sgMail from "@sendgrid/mail";
import { config } from "../config";

sgMail.setApiKey(config.sendgridApiKey);

export async function sendOrderConfirmation(email: string, orderId: number): Promise<boolean> {
  try {
    await sgMail.send({
      to: email,
      from: "shop@example.com",
      subject: `Order #${orderId} confirmed`,
      html: `<p>Your order #${orderId} has been confirmed.</p>`,
    });
  } catch {
    // BUG 12: error swallowed — no logging, no re-throw, returns success
  }
  return true;
}
