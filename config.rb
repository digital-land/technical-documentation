require 'govuk_tech_docs'

GovukTechDocs.configure(self)

class PlantUML < Middleman::Extension
  def initialize( app, options_hash = {}, &block)
    super
  end
  helpers do
    def plantuml(diagram_path)
      out, err, status = Open3.capture3(
        "java -jar #{__dir__}/.bin/plantuml.jar -pipe -tsvg",
        {
        stdin_data: File.read("#{__dir__}/source/#{diagram_path}"),
        chdir: "#{__dir__}/source/#{File.dirname(diagram_path)}"
        }
      )
      svg = out.gsub( /.*<svg/m, "<svg" ).gsub(/\n/, '').gsub(/<!--(.|\s)*?-->/m, "")
      concat_content(svg.html_safe)
    end
  end
end

::Middleman::Extensions.register(:plantuml, PlantUML)

activate :plantuml

configure :build do
  activate :relative_assets
  set :relative_links, true
  set :site_url, "/technical-documentation"
end
