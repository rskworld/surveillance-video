# Project: Surveillance Video Dataset
# Author: Molla Samser
# Website: https://rskworld.in/
# Contact: help@rskworld.in
# Phone: +91 93305 39277
# Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

"""
Alert and notification system for surveillance video monitoring.
Supports real-time alerts, email notifications, and alert management.
"""

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
import argparse


class AlertSystem:
    """Alert and notification system."""
    
    def __init__(self, config_file='config/alert_config.json'):
        self.alerts = []
        self.config = self.load_config(config_file)
        self.alert_history = []
    
    def load_config(self, config_file):
        """Load alert configuration."""
        default_config = {
            'email': {
                'enabled': False,
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'username': '',
                'password': '',
                'recipients': []
            },
            'alert_rules': {
                'anomaly_detected': True,
                'multiple_persons': True,
                'person_count_threshold': 3,
                'quality_below_threshold': True,
                'quality_threshold': 50
            },
            'notification_channels': ['console', 'file']
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def check_anomalies(self, anomalies_file='annotations/anomalies.json'):
        """Check for anomalies and trigger alerts."""
        if not os.path.exists(anomalies_file):
            return
        
        with open(anomalies_file, 'r') as f:
            data = json.load(f)
        
        anomalies = data.get('anomalies', [])
        
        for anomaly in anomalies:
            if anomaly.get('severity') in ['high', 'critical']:
                self.trigger_alert(
                    'anomaly_detected',
                    f"High severity anomaly detected: {anomaly.get('type')}",
                    {
                        'anomaly_id': anomaly.get('id'),
                        'type': anomaly.get('type'),
                        'start_time': anomaly.get('start_time'),
                        'severity': anomaly.get('severity'),
                        'video': data.get('video_id')
                    }
                )
    
    def check_person_count(self, detections_file='annotations/person_detections.json'):
        """Check person count and trigger alerts if threshold exceeded."""
        if not os.path.exists(detections_file):
            return
        
        threshold = self.config['alert_rules'].get('person_count_threshold', 3)
        
        with open(detections_file, 'r') as f:
            data = json.load(f)
        
        for detection in data.get('detections', []):
            person_count = len(detection.get('persons', []))
            
            if person_count >= threshold:
                self.trigger_alert(
                    'multiple_persons',
                    f"Multiple persons detected: {person_count} (threshold: {threshold})",
                    {
                        'person_count': person_count,
                        'threshold': threshold,
                        'timestamp': detection.get('timestamp'),
                        'video': data.get('video_id')
                    }
                )
    
    def check_video_quality(self, quality_report='output/quality_report.json'):
        """Check video quality and trigger alerts if below threshold."""
        if not os.path.exists(quality_report):
            return
        
        threshold = self.config['alert_rules'].get('quality_threshold', 50)
        
        with open(quality_report, 'r') as f:
            reports = json.load(f)
        
        for report in reports:
            quality_score = report.get('quality_metrics', {}).get('overall_score', 100)
            
            if quality_score < threshold:
                self.trigger_alert(
                    'quality_below_threshold',
                    f"Video quality below threshold: {quality_score}/100 (threshold: {threshold})",
                    {
                        'quality_score': quality_score,
                        'threshold': threshold,
                        'video': report.get('filename')
                    }
                )
    
    def trigger_alert(self, alert_type, message, details=None):
        """Trigger an alert."""
        alert = {
            'id': len(self.alerts) + 1,
            'type': alert_type,
            'message': message,
            'details': details or {},
            'timestamp': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self.alerts.append(alert)
        self.alert_history.append(alert)
        
        # Send notifications
        self.send_notifications(alert)
        
        return alert
    
    def send_notifications(self, alert):
        """Send notifications through configured channels."""
        channels = self.config.get('notification_channels', ['console'])
        
        for channel in channels:
            if channel == 'console':
                self._send_console_notification(alert)
            elif channel == 'file':
                self._send_file_notification(alert)
            elif channel == 'email':
                self._send_email_notification(alert)
    
    def _send_console_notification(self, alert):
        """Send console notification."""
        print("\n" + "=" * 60)
        print("ALERT TRIGGERED")
        print("=" * 60)
        print(f"Type: {alert['type']}")
        print(f"Message: {alert['message']}")
        print(f"Timestamp: {alert['timestamp']}")
        if alert['details']:
            print(f"Details: {json.dumps(alert['details'], indent=2)}")
        print("=" * 60 + "\n")
    
    def _send_file_notification(self, alert):
        """Save alert to file."""
        os.makedirs('output', exist_ok=True)
        alert_file = f"output/alerts_{datetime.now().strftime('%Y%m%d')}.json"
        
        alerts_today = []
        if os.path.exists(alert_file):
            with open(alert_file, 'r') as f:
                alerts_today = json.load(f)
        
        alerts_today.append(alert)
        
        with open(alert_file, 'w') as f:
            json.dump(alerts_today, f, indent=2)
    
    def _send_email_notification(self, alert):
        """Send email notification."""
        email_config = self.config.get('email', {})
        
        if not email_config.get('enabled'):
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = email_config.get('username')
            msg['To'] = ', '.join(email_config.get('recipients', []))
            msg['Subject'] = f"Surveillance Alert: {alert['type']}"
            
            body = f"""
            Alert Type: {alert['type']}
            Message: {alert['message']}
            Timestamp: {alert['timestamp']}
            
            Details:
            {json.dumps(alert['details'], indent=2)}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(email_config.get('smtp_server'), email_config.get('smtp_port'))
            server.starttls()
            server.login(email_config.get('username'), email_config.get('password'))
            server.send_message(msg)
            server.quit()
            
            print(f"Email notification sent for alert {alert['id']}")
        except Exception as e:
            print(f"Failed to send email notification: {e}")
    
    def get_active_alerts(self):
        """Get all active alerts."""
        return [a for a in self.alerts if a.get('status') == 'active']
    
    def resolve_alert(self, alert_id):
        """Mark an alert as resolved."""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['status'] = 'resolved'
                alert['resolved_at'] = datetime.now().isoformat()
                return True
        return False
    
    def generate_alert_report(self, output_file='output/alert_report.json'):
        """Generate alert report."""
        report = {
            'total_alerts': len(self.alert_history),
            'active_alerts': len(self.get_active_alerts()),
            'resolved_alerts': len([a for a in self.alert_history if a.get('status') == 'resolved']),
            'alerts_by_type': {},
            'recent_alerts': self.alert_history[-10:],
            'timestamp': datetime.now().isoformat()
        }
        
        # Count alerts by type
        for alert in self.alert_history:
            alert_type = alert['type']
            report['alerts_by_type'][alert_type] = report['alerts_by_type'].get(alert_type, 0) + 1
        
        os.makedirs('output', exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report


def create_sample_alert_config():
    """Create sample alert configuration."""
    config = {
        'email': {
            'enabled': False,
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': 'your_email@gmail.com',
            'password': 'your_app_password',
            'recipients': ['admin@example.com']
        },
        'alert_rules': {
            'anomaly_detected': True,
            'multiple_persons': True,
            'person_count_threshold': 3,
            'quality_below_threshold': True,
            'quality_threshold': 50
        },
        'notification_channels': ['console', 'file']
    }
    
    os.makedirs('config', exist_ok=True)
    with open('config/alert_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Sample alert configuration created: config/alert_config.json")


def main():
    parser = argparse.ArgumentParser(description='Alert and notification system')
    parser.add_argument('--config', '-c', default='config/alert_config.json',
                       help='Alert configuration file')
    parser.add_argument('--create-config', action='store_true',
                       help='Create sample alert configuration')
    parser.add_argument('--check-anomalies', action='store_true',
                       help='Check for anomalies')
    parser.add_argument('--check-persons', action='store_true',
                       help='Check person count')
    parser.add_argument('--check-quality', action='store_true',
                       help='Check video quality')
    parser.add_argument('--check-all', action='store_true',
                       help='Run all checks')
    parser.add_argument('--report', '-r', action='store_true',
                       help='Generate alert report')
    
    args = parser.parse_args()
    
    if args.create_config:
        create_sample_alert_config()
        return
    
    alert_system = AlertSystem(args.config)
    
    if args.check_all or args.check_anomalies:
        alert_system.check_anomalies()
    
    if args.check_all or args.check_persons:
        alert_system.check_person_count()
    
    if args.check_all or args.check_quality:
        alert_system.check_video_quality()
    
    if args.report:
        report = alert_system.generate_alert_report()
        print("\nAlert Report:")
        print(f"  Total Alerts: {report['total_alerts']}")
        print(f"  Active Alerts: {report['active_alerts']}")
        print(f"  Resolved Alerts: {report['resolved_alerts']}")
        print(f"  Alerts by Type: {report['alerts_by_type']}")


if __name__ == '__main__':
    main()

