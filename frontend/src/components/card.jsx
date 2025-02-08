import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import CardActionArea from '@mui/material/CardActionArea';

// Reusable Card Component with Props
export default function ActionAreaCard({ image, title, description }) {
  return (
    <div p-10>
      <Card sx={{ maxWidth: 345 }}>
        <CardActionArea>
          <CardMedia
            component="img"
            sx={{ height: 200, width: '100%', objectFit: 'cover' }} // Fixed size with aspect ratio maintained
            image={image}
            alt={title}
          />
          <CardContent>
            <Typography gutterBottom variant="h5" component="div">
              {title}
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              {description}
            </Typography>
          </CardContent>
        </CardActionArea>
      </Card>
    </div>
  );
}
