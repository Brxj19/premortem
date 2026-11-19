// Stub type declarations for third-party modules used in fixtures.
// The fixtures only need to parse (tsc --noEmit), not run.

declare module "stripe" {
  namespace Stripe {
    interface Charge { id: string; }
    interface Refund { id: string; }
    interface ChargeCreateParams { amount: number; currency: string; source: string; description: string; }
    interface RefundCreateParams { charge: string; amount: number; }
  }
  class Stripe {
    constructor(key: string, opts?: { apiVersion: string });
    charges: { create(params: Stripe.ChargeCreateParams): Promise<Stripe.Charge> };
    refunds: { create(params: Stripe.RefundCreateParams): Promise<Stripe.Refund> };
  }
  export = Stripe;
}

declare module "ioredis" {
  class Redis {
    constructor(url: string);
    get(key: string): Promise<string | null>;
    set(key: string, value: string): Promise<string>;
    setex(key: string, ttl: number, value: string): Promise<string>;
  }
  export = Redis;
}

declare module "@aws-sdk/client-s3" {
  export class S3Client { constructor(config: { region: string }); send(cmd: any): Promise<any>; }
  export class PutObjectCommand { constructor(params: { Bucket: string; Key: string; Body: any }); }
}

declare module "@sendgrid/mail" {
  const sgMail: {
    setApiKey(key: string): void;
    send(msg: { to: string; from: string; subject: string; html: string }): Promise<any>;
  };
  export = sgMail;
}

declare module "bullmq" {
  export class Worker {
    constructor(name: string, handler: (job: { data: any }) => Promise<void>);
  }
}

declare module "axios" {
  interface AxiosInstance {
    post(url: string, data?: any): Promise<{ data: any }>;
  }
  const axios: AxiosInstance & {
    create(config: { baseURL: string; timeout: number }): AxiosInstance;
  };
  export = axios;
}

declare module "p-retry" {
  function pRetry<T>(fn: () => Promise<T>, opts?: { retries: number }): Promise<T>;
  export = pRetry;
}

declare module "multer" {
  import { RequestHandler } from "express";
  interface Multer { single(field: string): RequestHandler; }
  function multer(opts?: any): Multer;
  export = multer;
}

declare module "zod" {
  export const z: {
    object(shape: any): { parse(data: any): any };
    string(): any;
    number(): { positive(): any; int(): { nonneg(): any } };
  };
}

declare module "@prisma/client" {
  interface PrismaClient {
    order: any;
    product: any;
    refund: any;
    upload: any;
    $transaction(fn: (tx: any) => Promise<any>): Promise<any>;
  }
  class PrismaClient { constructor(); }
  export { PrismaClient };
}

declare module "next/server" {
  export class NextRequest {
    headers: { get(name: string): string | null };
    json(): Promise<any>;
  }
  export class NextResponse {
    static json(data: any, init?: { status?: number }): NextResponse;
  }
}
