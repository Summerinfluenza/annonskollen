export class PythonApiService {
  async checkHealth() {
    try {
      const res = await fetch('http://127.0.0.1:8000/');
      return res.ok;
    } catch {
      return false;
    }
  }
}