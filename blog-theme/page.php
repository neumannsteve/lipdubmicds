<div id="content" class="widecolumn">
<?php if (have_posts()) : while (have_posts()) : the_post();?>
<div class="gallery">
<?php the_content('<p class="serif">Read the rest of this page &raquo;</p>'); ?>
</div>
<?php endwhile; endif; ?>
</div>
<?php get_footer(); ?>
