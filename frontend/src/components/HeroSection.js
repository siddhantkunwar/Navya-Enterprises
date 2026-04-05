export default function HeroSection({ image, title, subtitle }) {
  return (
    <section data-testid="hero-section" className="relative h-[50vh] min-h-[360px] max-h-[500px] overflow-hidden">
      <img
        src={image}
        alt={title}
        className="absolute inset-0 w-full h-full object-cover"
      />
      <div className="hero-overlay absolute inset-0" />
      <div className="relative z-10 h-full flex flex-col items-center justify-center text-center px-4">
        <h1
          data-testid="hero-title"
          className="font-heading text-4xl sm:text-5xl lg:text-6xl text-white font-bold tracking-tight opacity-0 animate-fade-in"
        >
          {title}
        </h1>
        {subtitle && (
          <p
            data-testid="hero-subtitle"
            className="mt-4 text-sage/90 text-lg sm:text-xl max-w-2xl font-light opacity-0 animate-fade-in stagger-2"
          >
            {subtitle}
          </p>
        )}
      </div>
    </section>
  );
}
