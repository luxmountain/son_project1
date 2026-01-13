"""
Service Proxy for API Gateway
Handles routing requests to downstream services
"""
import requests
from django.conf import settings
from typing import Optional, Dict, Any


class ServiceProxy:
    """Proxy for routing requests to downstream services"""
    
    def __init__(self):
        self.services = getattr(settings, 'SERVICES', {})
        self.timeout = 10
    
    def _get_service_url(self, service_name: str) -> Optional[str]:
        """Get service URL from configuration"""
        return self.services.get(service_name)
    
    def _make_request(
        self, 
        method: str, 
        service_name: str, 
        path: str, 
        data: Dict = None, 
        params: Dict = None
    ) -> Dict[str, Any]:
        """Make request to downstream service"""
        base_url = self._get_service_url(service_name)
        if not base_url:
            return {
                'success': False,
                'status_code': 503,
                'error': f'Service {service_name} not configured'
            }
        
        url = f"{base_url}/api/{path}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data if method in ['POST', 'PUT', 'PATCH'] else None,
                params=params,
                timeout=self.timeout
            )
            
            return {
                'success': True,
                'status_code': response.status_code,
                'data': response.json() if response.content else None
            }
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'status_code': 504,
                'error': f'Service {service_name} timeout'
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'status_code': 503,
                'error': f'Service {service_name} unavailable'
            }
        except Exception as e:
            return {
                'success': False,
                'status_code': 500,
                'error': str(e)
            }
    
    def get(self, service_name: str, path: str, params: Dict = None) -> Dict[str, Any]:
        return self._make_request('GET', service_name, path, params=params)
    
    def post(self, service_name: str, path: str, data: Dict = None) -> Dict[str, Any]:
        return self._make_request('POST', service_name, path, data=data)
    
    def put(self, service_name: str, path: str, data: Dict = None) -> Dict[str, Any]:
        return self._make_request('PUT', service_name, path, data=data)
    
    def patch(self, service_name: str, path: str, data: Dict = None) -> Dict[str, Any]:
        return self._make_request('PATCH', service_name, path, data=data)
    
    def delete(self, service_name: str, path: str) -> Dict[str, Any]:
        return self._make_request('DELETE', service_name, path)
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of all services"""
        results = {}
        for service_name, base_url in self.services.items():
            try:
                response = requests.get(f"{base_url}/health/", timeout=2)
                results[service_name] = {
                    'healthy': response.status_code == 200,
                    'status_code': response.status_code
                }
            except:
                results[service_name] = {
                    'healthy': False,
                    'error': 'Connection failed'
                }
        return results


# Singleton instance
service_proxy = ServiceProxy()
