import axios from 'axios';

export class PythonApiService {
  private readonly baseUrl = 'http://127.0.0.1:8000/api/v1';

  async checkHealth() {
    try {
      const response = await axios.get(`${this.baseUrl.replace('/api/v1', '')}/`);
      return response.status === 200;
    } catch {
      return false;
    }
  }
}