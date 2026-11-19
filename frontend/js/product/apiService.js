export class ApiService {
  static async GET(url, params = {}) {

    const query = new URLSearchParams(params).toString();
    const fullUrl = query ? `${url}?${query}` : url;

    const response = await fetch(fullUrl);

    if (!response.ok) {
      throw new Error(`Ошибка запроса: HTTP ${response.status}`);
    }

    return response.json();
  }
}
