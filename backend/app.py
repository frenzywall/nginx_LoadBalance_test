from flask import Flask, render_template_string, request, jsonify
import os
import platform
import psutil
import datetime
import socket
import time

app = Flask(__name__)
INSTANCE_ID = os.getenv("INSTANCE_ID", "unknown")


BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>System Monitor</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.0/chart.min.js"></script>
    <style>
        :root {
            --primary: #1976D2;
            --success: #4CAF50;
            --warning: #FFC107;
            --danger: #f44336;
        }
        
        body {
            font-family: system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-decoration: none;
            color: inherit;
            transition: transform 0.2s;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
        }
        
        .stat-card h2 {
            margin: 0;
            font-size: 1.1em;
            color: #666;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .stat-card .value {
            font-size: 1.8em;
            font-weight: bold;
            color: var(--primary);
            margin: 0.5em 0;
        }
        
        .stat-card .label {
            color: #666;
            font-size: 0.9em;
        }
        
        .preview-chart {
            height: 4px;
            background: #eee;
            margin-top: 1em;
            border-radius: 2px;
        }
        
        .preview-bar {
            height: 100%;
            border-radius: 2px;
            transition: width 0.3s ease;
        }
        
        .preview-bar.success { background: var(--success); }
        .preview-bar.warning { background: var(--warning); }
        .preview-bar.danger { background: var(--danger); }
        
        .health-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            display: inline-block;
            vertical-align: middle;
        }
        
        .health-indicator.success { background: var(--success); }
        .health-indicator.warning { background: var(--warning); }
        .health-indicator.danger { background: var(--danger); }
        
        .instance-badge {
            display: inline-block;
            padding: 0.25em 0.75em;
            background: #e8f5e9;
            color: var(--primary);
            border-radius: 12px;
            margin-top: 1em;
            font-size: 0.875em;
            font-weight: 500;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin: 1em 0;
        }
        
        .metric-item {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 6px;
            text-align: center;
        }
        
        .metric-label {
            font-size: 0.875em;
            color: #666;
            margin-bottom: 4px;
        }
        
        .metric-value {
            font-size: 1.25em;
            font-weight: 600;
            color: var(--primary);
        }
        
        .system-info {
            margin-top: 2em;
            padding: 1em;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 16px;
            margin-top: 1em;
        }
        
        .info-item {
            padding: 8px;
        }
        
        .info-label {
            font-size: 0.875em;
            color: #666;
        }
        
        .info-value {
            font-size: 1em;
            color: #333;
            margin-top: 4px;
        }
    </style>
</head>
<body>
    {{ content | safe }}
</body>
</html>
"""

def get_system_info():
    return {
        'os': f"{platform.system()} {platform.release()}",
        'python': platform.python_version(),
        'processor': platform.processor() or 'Unknown',
        'cpu_cores': psutil.cpu_count(logical=False),
        'cpu_threads': psutil.cpu_count(logical=True),
        'total_memory': f"{psutil.virtual_memory().total / (1024**3):.1f}GB",
        'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
    }

def get_disk_info():
    disk = psutil.disk_usage('/')
    return {
        'total': f"{disk.total / (1024**3):.1f}GB",
        'used': f"{disk.used / (1024**3):.1f}GB",
        'free': f"{disk.free / (1024**3):.1f}GB",
        'percent': disk.percent
    }
@app.route('/metrics')
def metrics():
    psutil.cpu_percent()  
    time.sleep(0.1)  
    metrics_data = {
        'cpu': psutil.cpu_percent(),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'uptime': time.time() - psutil.boot_time(),
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(metrics_data)


@app.route('/api/stats')
def api_stats():
   
    psutil.cpu_percent()
    time.sleep(0.1)  
    
    return jsonify({
        'cpu': psutil.cpu_percent(),
        'memory': psutil.virtual_memory().percent,
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'disk': psutil.disk_usage('/').percent
    })

@app.route('/health')
def health():
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = get_disk_info()
    
    def get_status_class(value, warning=70, danger=80):
        if value >= danger:
            return 'danger'
        elif value >= warning:
            return 'warning'
        return 'success'
    
    uptime_seconds = time.time() - psutil.boot_time()
    days = int(uptime_seconds // (24 * 3600))
    hours = int((uptime_seconds % (24 * 3600)) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    
    content = f"""
    <div class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <h2>
                    <span class="health-indicator {get_status_class(cpu_percent)}"></span>
                    System Status
                </h2>
                <div class="value">{cpu_percent}% CPU Usage</div>
                <div class="label">{'Critical' if cpu_percent >= 35 else 'Warning' if cpu_percent >= 20 else 'Healthy'}</div>
                <div class="preview-chart">
                    <div class="preview-bar {get_status_class(cpu_percent)}" style="width: {cpu_percent}%"></div>
                </div>
            </div>
            
            <div class="stat-card">
                <h2>
                    <span class="health-indicator {get_status_class(memory.percent)}"></span>
                    Memory Status
                </h2>
                <div class="value">{memory.percent}% Used</div>
                <div class="label">{memory.available / (1024**3):.1f}GB Available</div>
                <div class="preview-chart">
                    <div class="preview-bar {get_status_class(memory.percent)}" style="width: {memory.percent}%"></div>
                </div>
            </div>
            
            <div class="stat-card">
                <h2>
                    <span class="health-indicator {get_status_class(disk['percent'])}"></span>
                    Storage Status
                </h2>
                <div class="value">{disk['percent']}% Used</div>
                <div class="label">{disk['free']} Available</div>
                <div class="preview-chart">
                    <div class="preview-bar {get_status_class(disk['percent'])}" style="width: {disk['percent']}%"></div>
                </div>
            </div>
        </div>
        
        <div class="system-info">
            <h2>System Information</h2>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Uptime</div>
                    <div class="info-value">{days}d {hours}h {minutes}m</div>
                </div>
                <div class="info-item">
                    <div class="info-label">OS</div>
                    <div class="info-value">{get_system_info()['os']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">CPU Info</div>
                    <div class="info-value">{get_system_info()['cpu_cores']} cores, {get_system_info()['cpu_threads']} threads</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Total Memory</div>
                    <div class="info-value">{get_system_info()['total_memory']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Boot Time</div>
                    <div class="info-value">{get_system_info()['boot_time']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Python Version</div>
                    <div class="info-value">{get_system_info()['python']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Instance-ID</div>
                    <div class="info-value">{INSTANCE_ID}</div>
                </div>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/')
def index():
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = get_disk_info()
    system_info = get_system_info()
    
    def get_status_class(value, warning=70, danger=80):
        if value >= danger:
            return 'danger'
        elif value >= warning:
            return 'warning'
        return 'success'
    
    content = f"""
    <div class="container">
        <div class="stats-grid">
            <a href="/metrics" class="stat-card">
                <h2>System Metrics</h2>
                <div class="value">Real-time Monitor</div>
                <div class="label">CPU, Memory & Disk Usage</div>
                <div class="preview-chart">
                    <div class="preview-bar {get_status_class(cpu_percent)}" style="width: {cpu_percent}%"></div>
                </div>
            </a>
            
            <a href="/health" class="stat-card">
                <h2>Health Status</h2>
                <div class="value">System Health</div>
                <div class="label">Detailed System Information</div>
                <div class="health-indicator {get_status_class(max(cpu_percent, memory.percent, disk['percent']))}"></div>
            </a>
            
            <div class="stat-card">
                <h2>You are on</h2>
                <div class="value">Instance-{INSTANCE_ID}</div>
                <div class="label">{socket.gethostname()}</div>
                <div class="instance-badge">Active</div>
            </div>
        </div>
        
        <div class="metric-grid">
            <div class="metric-item">
                <div class="metric-label">CPU Usage</div>
                <div class="metric-value">{cpu_percent}%</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Memory Usage</div>
                <div class="metric-value">{memory.percent}%</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Disk Usage</div>
                <div class="metric-value">{disk['percent']}%</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">OS</div>
                <div class="metric-value">{system_info['os'].split()[0]}</div>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, content=content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)