import { BadRequestException, Injectable } from "@nestjs/common";

interface PendingCode {
  code: string;
  expiresAt: number;
}

@Injectable()
export class AuthService {
  private readonly pendingCodes = new Map<string, PendingCode>();
  private readonly expiresInMs = this.resolveExpiresInMs();

  private resolveExpiresInMs(): number {
    const parsed = Number(process.env.AUTH_CODE_EXPIRES_SECONDS ?? 300);
    if (Number.isFinite(parsed) && parsed > 0) {
      return parsed * 1000;
    }
    return 300 * 1000;
  }

  sendCode(email: string) {
    const code = Math.floor(100000 + Math.random() * 900000).toString();

    this.pendingCodes.set(email, {
      code,
      expiresAt: Date.now() + this.expiresInMs
    });

    return {
      sent: true,
      expiresInSeconds: this.expiresInMs / 1000,
      debugCode: code
    };
  }

  verifyCode(email: string, code: string) {
    const pending = this.pendingCodes.get(email);

    if (!pending) {
      throw new BadRequestException("No code found for this email");
    }

    if (pending.expiresAt < Date.now()) {
      this.pendingCodes.delete(email);
      throw new BadRequestException("Code expired");
    }

    if (pending.code !== code) {
      throw new BadRequestException("Invalid code");
    }

    this.pendingCodes.delete(email);

    const tokenPayload = JSON.stringify({
      email,
      loginAt: new Date().toISOString()
    });

    return {
      accessToken: Buffer.from(tokenPayload).toString("base64url")
    };
  }
}
