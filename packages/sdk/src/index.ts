export class BoardOsSdk {
  constructor(private readonly baseUrl: string) {}

  async health(): Promise<unknown> {
    const response = await fetch(`${this.baseUrl}/health`);
    return response.json();
  }
}

