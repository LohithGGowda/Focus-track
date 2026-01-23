# Manual Deployment Guide - Focus Track to EC2

## Prerequisites
- EC2 instance running Ubuntu with Python 3.10+
- SSH access to your instance
- PEM key: `react-ikey.pem`

## Step 1: SSH into EC2
```bash
ssh -i ~/Documents/week2-DMI/react-ikey.pem ubuntu@ec2-13-126-186-131.ap-south-1.compute.amazonaws.com
```

## Step 2: Update System and Install Dependencies
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git
```

## Step 3: Clone or Copy Your Repository
```bash
cd /home/ubuntu
git clone https://github.com/LohithGGowda/Focus-track.git
# OR if already copied, just navigate to it
cd /home/ubuntu/focus-track
```

## Step 4: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 5: Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 6: Create Instance Directory for Database
```bash
mkdir -p instance
```

## Step 7: Run the Application
### Option A: Simple Run (for testing)
```bash
python mainrun.py
```

### Option B: Run with Gunicorn (Production)
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 --workers=2 mainrun:app
```

## Step 8: Keep Application Running (Using nohup + crontab)

This is the simplest and most reliable approach for manual deployment.

First, kill any running processes:
```bash
pkill -f "gunicorn --bind"
```

Start gunicorn in the background:
```bash
cd /home/ubuntu/Focus-track
source venv/bin/activate
nohup gunicorn --bind 0.0.0.0:5000 --workers=2 mainrun:app > /tmp/focus-track.log 2>&1 &
```

Make it persistent across reboots by adding to crontab:
```bash
crontab -e
```

Add this line:
```
@reboot cd /home/ubuntu/Focus-track && source venv/bin/activate && nohup gunicorn --bind 0.0.0.0:5000 --workers=2 mainrun:app > /tmp/focus-track.log 2>&1 &
```

Save and exit (Ctrl+X, Y, Enter).

## Step 9: Verify Application is Running

Check if processes are running:
```bash
ps aux | grep gunicorn
```

Test the application:
```bash
curl http://localhost:5000/
```

View logs:
```bash
tail -f /tmp/focus-track.log
```

## Step 10: Access Your Application
- Open in browser: `http://ec2-13-126-186-131.ap-south-1.compute.amazonaws.com:5000`
- The 404 error is normal if you don't have a root route defined - just test your actual endpoints

## Step 11: Optional - Setup Nginx as Reverse Proxy

### Install Nginx
```bash
sudo apt install -y nginx
```

### Create Nginx Config
```bash
sudo nano /etc/nginx/sites-available/focus-track
```

Paste:
```nginx
server {
    listen 80;
    server_name ec2-13-126-186-131.ap-south-1.compute.amazonaws.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Enable Nginx
```bash
sudo ln -s /etc/nginx/sites-available/focus-track /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl start nginx
sudo systemctl enable nginx
```

Now access at: `http://ec2-13-126-186-131.ap-south-1.compute.amazonaws.com:80` (no port needed)

## Troubleshooting

### Stop the application
```bash
pkill -f "gunicorn --bind"
```

### Restart the application
```bash
pkill -f "gunicorn --bind"
cd /home/ubuntu/Focus-track
source venv/bin/activate
nohup gunicorn --bind 0.0.0.0:5000 --workers=2 mainrun:app > /tmp/focus-track.log 2>&1 &
```

### View application logs
```bash
tail -f /tmp/focus-track.log
```

### Check if port 5000 is in use
```bash
netstat -tuln | grep 5000
```

### Verify application responds
```bash
curl http://localhost:5000/
```
