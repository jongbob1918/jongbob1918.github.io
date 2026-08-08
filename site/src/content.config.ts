import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const notes = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/notes' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedAt: z.coerce.date(),
    updatedAt: z.coerce.date().optional(),
    category: z.enum([
      'robotics-foundations',
      'localization-slam',
      'planning-control',
      'ros2-systems',
      'projects'
    ]),
    type: z.enum(['overview', 'concept', 'algorithm', 'implementation', 'experiment', 'case-study']),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    featured: z.boolean().default(false)
  })
});

export const collections = { notes };
